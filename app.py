import boto3
import requests
import os
import threading
import time

from flask_cors import CORS
from flask import Flask, request
from model.samurai import Samurai
from model.samurai import MAX_SQL_RETRY

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

session = boto3.Session()
boto3_bedrock = boto3.client(service_name="bedrock-runtime")

vn = Samurai(client=boto3_bedrock)
vn.temperature = 0
vn.max_tokens = 4096

vn.connect_to_snowflake_v2()

# events map to dedupe events
events_map = {}

BOT_USER_ID = os.environ["BOT_USER_ID"]
HEADERS = {"Authorization": "Bearer {}".format(os.environ["BOT_USER_OAUTH_TOKEN"])}


def post_message(sink, text, thread_ts=None):
    body = {"channel": sink, "text": text, "thread_ts": thread_ts}

    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage", json=body, headers=HEADERS
        )

        if not response or response.status_code != 200 or not response.json().get("ok"):
            raise Exception(
                "Failed to post chat, request body: {}, response status: {}, response data: {}".format(
                    body, response.status_code, response.json()
                )
            )

        return response.json()
    except Exception as e:
        app.logger.error("Error posting message to {}".format(sink))
        app.logger.error(str(e))

    return None


def reply_message(sink, text, ts, broadcast):
    body = {
        "channel": sink,
        "text": text,
        "thread_ts": ts,
        "reply_broadcast": broadcast,
    }

    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            json=body,
            headers=HEADERS,
        )

        if not response or response.status_code != 200 or not response.json().get("ok"):
            raise Exception(
                "Failed to post chat, request body: {}, response status: {}, response data: {}".format(
                    body, response.status_code, response.json()
                )
            )

        return response.json()
    except Exception as e:
        app.logger.error("Error posting message to {}".format(sink))
        app.logger.error(str(e))

    return None


def upload_file_v2(sink, file_content, filename, title, initial_comment, ts):
    # Get upload URL
    try:
        upload_url_response = requests.get(
            "https://slack.com/api/files.getUploadURLExternal",
            headers=HEADERS,
            params={"filename": filename, "length": len(file_content)},
        )

        upload_url_data = upload_url_response.json()
        if (
            not upload_url_response
            or upload_url_response.status_code != 200
            or not upload_url_data.get("ok")
        ):
            raise Exception(
                "Failed to get upload URL, response status: {}, response data: {}".format(
                    upload_url_response.status_code, upload_url_data
                )
            )

        upload_url = upload_url_data["upload_url"]
        file_id = upload_url_data["file_id"]
    except Exception as e:
        app.logger.error("Error getting upload URL")
        app.logger.error(str(e))
        return None

    # Upload file to obtained URL
    try:
        upload_response = requests.post(upload_url, headers=HEADERS, data=file_content)

        if not upload_response or upload_response.status_code != 200:
            raise Exception(
                "Failed to upload file, response status: {}, response data: {}".format(
                    upload_response.status_code, upload_response.text
                )
            )
    except Exception as e:
        app.logger.error("Error uploading file")
        app.logger.error(str(e))
        return None

    # Complete the upload

    try:
        complete_upload_response = requests.post(
            "https://slack.com/api/files.completeUploadExternal",
            headers=HEADERS,
            json={
                "files": [{"id": file_id, "title": title}],
                "thread_ts": ts,
                "channel_id": sink,
            },
        )

        complete_upload_data = complete_upload_response.json()
        if (
            not complete_upload_response
            or complete_upload_response.status_code != 200
            or not complete_upload_data.get("ok")
        ):
            raise Exception(
                "Failed to complete upload, response status: {}, response data: {}".format(
                    complete_upload_response.status_code, complete_upload_data
                )
            )
    except Exception as e:
        app.logger.error("Error completing upload")
        app.logger.error(str(e))

    return None


# deprecated
def upload_file(sink, file_content, filename, title, initial_comment, ts):
    body = {
        "channels": sink,
        "file": file_content,
        "filename": filename,
        "title": title,
        "initial_comment": initial_comment,
        # 'thread_ts': ts,
        # 'reply_broadcast': True
    }

    try:
        response = requests.post(
            "https://slack.com/api/files.upload",
            data=body,
            headers=HEADERS,
            files={"file": file_content},
        )

        if not response or response.status_code != 200 or not response.json().get("ok"):
            raise Exception(
                "Failed to upload file, request body: {}, response status: {}, response data: {}".format(
                    body, response.status_code, response.json()
                )
            )

        return response.json()
    except Exception as e:
        app.logger.error("Error uploading file to {}".format(sink))
        app.logger.error(str(e))

    return None


def reply_message_with_delay(delay, sink, text, ts, broadcast):
    time.sleep(delay)
    reply_message(sink, text, ts, broadcast)


def sql_reply(question, sink, ts, previous_messages=None):
    sql = vn.generate_sql_v2(previous_messages, question, allow_llm_to_see_data=True)

    if not vn.is_sql_valid(sql):
        reply_message(sink, sql, ts, broadcast=False)
        return

    sql_retry_remaining = MAX_SQL_RETRY
    while sql_retry_remaining > 0:
        try:
            df = vn.run_sql(sql)
            slack_sql = "```\n" + sql + "\n```"
            reply_message(sink, slack_sql, ts, broadcast=False)
            break
        except Exception as e:
            print("ERROR running sql", e)
            if not previous_messages:
                previous_messages = []
            previous_messages.append({"role": "user", "content": question})
            slack_sql = "```\n" + sql + "\n```"
            previous_messages.append({"role": "assistant", "content": slack_sql})
            sql = vn.generate_sql_v2(
                previous_messages,
                f"Got the following error {e}, can you recheck syntax? - do not add comments to the sql query.",
                allow_llm_to_see_data=True,
            )
            sql_retry_remaining -= 1

            if sql_retry_remaining == 0:
                slack_sql = "```\n" + sql + "\n```"
                reply_message(sink, slack_sql, ts, broadcast=False)
                reply_message(
                    sink,
                    f":cry: Sorry! I encountered an error while executing the query in Snowflake.```{e}```",
                    ts,
                    broadcast=False,
                )
                return

    slack_table = "```\n" + df.head(10).to_markdown(index=False) + "\n...```"

    reply_message(sink, slack_table, ts, broadcast=False)

    # plotly_code = vn.generate_plotly_code_v2(
    #     previous_message=previous_messages, question=question, sql=sql, df=df
    # )
    fig = vn.get_plotly_figure_v2(df=df, plotly_code=None)

    if fig:
        img = fig.to_image(format="png", width=800, height=600, scale=2)
        upload_file_v2(sink, img, "plot.png", "Plot", question, ts)


@app.route("/")
def index():
    return "Samurai Slack backend is up"


@app.route("/event", methods=["POST"])
def handle_events():
    data = request.get_json()
    # Verify the event route.
    if data["type"] == "url_verification":
        return data["challenge"]

    event_id = data["event_id"]
    if event_id in events_map:
        return ""
    events_map[event_id] = True

    if data["type"] == "event_callback" and "event" in data:
        if data["event"]["user"] != BOT_USER_ID:
            return handle_thread_replies(data)
        else:
            return ""
    else:
        print(f"unhandled data event: {data}")

    # Fallback.
    return ""


def handle_thread_replies(data):
    try:
        channel = data["event"]["channel"]
        thread_ts = data["event"]["thread_ts"]
        text = data["event"]["text"]
        response = requests.post(
            "https://slack.com/api/conversations.replies",
            params={
                "channel": channel,
                "ts": thread_ts,
            },
            headers=HEADERS,
        )

        if not response or response.status_code != 200 or not response.json().get("ok"):
            raise Exception(
                "Failed to get conversations response status: {}, response data: {}".format(
                    response.status_code, response.json()
                )
            )

        messages = response.json()["messages"]
        chat_messages = []
        is_first = True
        for message in messages[:-1]:
            if "text" not in message:
                continue
            if (
                message["user"] == BOT_USER_ID
                and not is_first
                and message["text"].strip() != ""
            ):
                chat_messages.append({"role": "assistant", "content": message["text"]})
            else:
                txt = message["text"]
                if not txt:
                    continue
                if is_first:
                    txt = message["text"].split('"')[1]
                    chat_messages.append({"role": "user", "content": txt})
                else:
                    chat_messages.append({"role": "user", "content": txt})
            is_first = False
        sql_reply(text, channel, thread_ts, chat_messages)
        return ("", 200)

    except Exception as e:
        app.logger.error("Error getting conversations")
        app.logger.error(str(e))
    return ("", 500)


@app.route("/slash", methods=["POST"])
def handle_slash():
    data = request.form

    # Post the command + text that was entered by the user.
    # post_message_resp = post_message(data['channel_id'], '{} {}'.format(data['command'], data['text']))
    post_message_resp = post_message(
        data["channel_id"], '<@{}> asked "{}"'.format(data["user_id"], data["text"])
    )

    # Post the first reply.
    # reply_message(data['channel_id'], sql, post_message_resp['ts'])
    x = threading.Thread(
        target=sql_reply,
        args=(data["text"], data["channel_id"], post_message_resp["ts"]),
    )
    x.start()

    # Post the second reply after a delay of 5s.
    # x = threading.Thread(target=reply_message_with_delay, args=(5, data['channel_id'], 'My Message 2', post_message_resp['ts']))
    # x.start()

    return ("", 200)


# main driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
