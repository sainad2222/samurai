import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from model.samurai import Samurai
import boto3

from dotenv import load_dotenv

load_dotenv()


session = boto3.Session()
boto3_bedrock = boto3.client(service_name="bedrock-runtime")

vn = Samurai(client=boto3_bedrock)

vn.train(
    question="""How many users faced add funds to wallet failure beacuse of failing to transfer funds to pool account on 16th July ? / How many users failed to add funds to wallet because of transfer funds to pool account failure?""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY: This table contains daily user activity data, including information about failed "Add Funds" transactions and the corresponding failure reasons.
Columns used: created_date_ist, failure_reason_add_fund, actor_id.
created_date_ist = '2024-07-16': Filters for activity on July 16, 2024.
failure_reason_add_fund = 'WALLET_ORDER_FAILURE_REASON_ERROR_TRANSFERRING_AMOUNT_TO_POOL_ACCOUNT': Filters for failed "Add Funds" transactions due to the specific failure reason of "Error transferring to pool account because the payment has failed."
count(distinct actor_id): Counts the distinct users (actor_id) who faced this specific failure reason on July 16, 2024.

Approach:
1. Filter the `USS_USER_DAILY` table for activity on July 16, 2024.
2. Filter for rows where the `failure_reason_add_fund` column has the value 'WALLET_ORDER_FAILURE_REASON_ERROR_TRANSFERRING_AMOUNT_TO_POOL_ACCOUNT'.
3. Count the distinct users (actor_id) to determine the number of users who faced this specific failure reason on that day.
*/
select count(distinct actor_id)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY
where created_date_ist = '2024-07-16'
and failure_reason_add_fund = 'WALLET_ORDER_FAILURE_REASON_ERROR_TRANSFERRING_AMOUNT_TO_POOL_ACCOUNT';



""",
)
vn.train(
    question="""My actor ID is "1b2eb76-4a90-b406-7430c0eb99d0", can you give me how much I have invested in Semiconductor stocks?""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: txn_amount_confirmed_usd, txn_created_month, type, txn_status, market_category_name, actor_id.
txn_created_month >= date_trunc(month, dateadd(month, -2, current_date()))): Filters for transactions that occurred in the last two months (including the current month).
type = 'BUY': Filters for transactions where the order type is a "BUY" order.
txn_status = 'ORDER_SUCCESS': Filters for transactions where the order was successfully completed.
market_category_name ilike '%semiconductor%`': Filters for transactions involving stocks in the "semiconductor" market category (case-insensitive).
actor_id = '1b2eb76-4a90-b406-7430c0eb99d0'`: Filters for transactions made by a specific user with the actor ID '1b2eb76-4a90-b406-7430c0eb99d0'.
sum(txn_amount_confirmed_usd): Calculates the sum of the confirmed transaction amounts in USD (txn_amount_confirmed_usd) for successful "BUY" orders made by the specified user within the last two months involving stocks in the semiconductor market category.

Approach:
1. Filter the USS_TRANSACTIONS table to include only successful "BUY" orders made by the specified user within the last two months involving stocks in the semiconductor market category.
2. Calculate the sum of the confirmed transaction amounts (txn_amount_confirmed_usd) for those orders.
*/
select sum(txn_amount_confirmed_usd)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where 1=1 
  and txn_created_month >= date_trunc(month, dateadd(month, -2, current_date()))
  and type = 'BUY'
  and txn_status = 'ORDER_SUCCESS'
  and market_category_name ilike '%semiconductor%'
  and actor_id = '1b2eb76-4a90-b406-7430c0eb99d0'""",
)
