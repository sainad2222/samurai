import boto3
import requests
import os
import threading
import time

from flask_cors import CORS
from flask import Flask, request
from model.samurai import Samurai

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

session = boto3.Session()
boto3_bedrock = boto3.client(service_name="bedrock-runtime")

vn = Samurai(client=boto3_bedrock)

vn.connect_to_snowflake_v2()

BOT_USER_ID = "U07DVEJ00NL"


def post_message(sink, text, thread_ts=None):
    body = {"channel": sink, "text": text, "thread_ts": thread_ts}

    try:
        response = requests.post(
            "https://slack.com/api/chat.postMessage",
            json=body,
            headers={
                "Authorization": "Bearer {}".format(os.environ["BOT_USER_OAUTH_TOKEN"])
            },
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
            headers={
                "Authorization": "Bearer {}".format(os.environ["BOT_USER_OAUTH_TOKEN"])
            },
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
            headers={
                "Authorization": "Bearer {}".format(os.environ["BOT_USER_OAUTH_TOKEN"])
            },
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


def sql_reply(question, sink, ts):
    sql = vn.generate_sql(question, allow_llm_to_see_data=True)

    slack_sql = "```\n" + sql + "\n```"

    reply_message(sink, slack_sql, ts, broadcast=False)

    df = vn.run_sql(sql)

    slack_table = "```\n" + df.head(10).to_markdown(index=False) + "\n...```"

    reply_message(sink, slack_table, ts, broadcast=False)

    plotly_code = vn.generate_plotly_code(question=question, sql=sql, df=df)
    fig = vn.get_plotly_figure_v2(plotly_code=plotly_code, df=df)

    img = fig.to_image(format="png", width=800, height=600, scale=2)

    upload_file(sink, img, "plot.png", "Plot", question, ts)


@app.route("/")
def index():
    return "Samurai Slack backend is up"


@app.route("/event", methods=["POST"])
def handle_events():
    data = request.get_json()
    # Verify the event route.
    if data["type"] == "url_verification":
        return data["challenge"]

    if data["type"] == "event_callback" and data["event"]["user"] != BOT_USER_ID:
        return handle_thread_replies(data)

    # Fallback.
    return ""


def handle_thread_replies(data):
    channel = data["event"]["channel"]
    thread_ts = data["event"]["thread_ts"]
    text = data["event"]["text"]
    try:
        response = requests.post(
            "https://slack.com/api/conversations.replies",
            params={
                "channel": channel,
                "ts": thread_ts,
            },
            headers={
                "Authorization": "Bearer {}".format(os.environ["BOT_USER_OAUTH_TOKEN"])
            },
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
        for message in messages:
            if message["user"] == BOT_USER_ID and not is_first:
                chat_messages.append({"role": "assistant", "content": message["text"]})
            else:
                txt = message["text"]
                if is_first:
                    txt = message["text"].split('"')[1]
                    chat_messages.append(txt)
                else:
                    chat_messages.append({"role": "user", "content": txt})
            is_first = False
        v2_response = vn.generate_sql_v2(
            chat_messages, text, allow_llm_to_see_data=True
        )
        post_message(channel, v2_response, thread_ts=thread_ts)
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
        data["channel_id"], 'I was asked "{}"'.format(data["text"])
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
