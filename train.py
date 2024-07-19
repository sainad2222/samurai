from model import Samurai
import boto3


session = boto3.Session()
boto3_bedrock = boto3.client(service_name="bedrock-runtime")

vn = Samurai(client=boto3_bedrock)
vn.train(
    ddl="""
create or replace TRANSIENT TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS (
        TABLE_REFRESH_TIME TIMESTAMP_LTZ(9),
        ACTOR_ID VARCHAR(16777216),
        TXN_ID VARCHAR(16777216),
        CLIENT_ORDER_ID VARCHAR(16777216), 
        VENDOR_ORDER_ID VARCHAR(16777216),
        VENDOR_ACCOUNT_ID VARCHAR(16777216),
        POOL_TXN_ORDER_ID VARCHAR(16777216),
        WF_REQ_ID VARCHAR(16777216),
        TYPE VARCHAR(16777216),
        TXN_STATUS VARCHAR(16777216),
        TXN_CREATED_TIME_IST TIMESTAMP_NTZ(9),
        TXN_UPDATED_TIME_IST TIMESTAMP_NTZ(9),
        TXN_CREATED_DATE DATE,
        TXN_UPDATED_DATE DATE,
        TXN_CREATED_WEEK DATE,
        TXN_CREATED_MONTH DATE,
        TXN_AMOUNT_REQUESTED_USD NUMBER(38,6),
        TXN_AMOUNT_CONFIRMED_USD NUMBER(38,6),
        QTY_REQUESTED FLOAT,
        QTY_CONFIRMED FLOAT,
        STOCK_PRICE_AT_REQUESTED_USD FLOAT,
        STOCK_PRICE_AT_CONFIRMED_USD FLOAT,
        STOCK_SYMBOL VARCHAR(16777216),
        STOCK_ID VARCHAR(16777216),
        STOCK_EXCHANGE VARCHAR(16777216),
        STOCK_INTERNAL_STATUS VARCHAR(16777216),
        STOCK_CREATED_TIME_IST TIMESTAMP_NTZ(9),
        STOCK_UPDATED_TIME_IST TIMESTAMP_NTZ(9),
        MARKET_CATEGORY_NAME VARCHAR(16777216),
        STOCK_COMPANY_NAME VARCHAR(16777216),
        STOCK_INDUSTRY_ID VARCHAR(16777216),
        STOCK_INDUSTRY_GROUP_ID VARCHAR(16777216),
        STOCK_SECTOR_ID VARCHAR(16777216),
        WORKFLOW_STAGE VARCHAR(16777216),
        WORKFLOW_STATUS VARCHAR(16777216),
        WORKFLOW_VERSION VARCHAR(16777216),
        WORKFLOW_TYPE VARCHAR(16777216),
        ACCOUNT_ID VARCHAR(16777216),
        ACCOUNT_CREATED_TIME_IST TIMESTAMP_NTZ(9),
        DAYS_SINCE_ACCOUNT_CREATION NUMBER(9,0),
        FIRST_INVEST_TIME_IST TIMESTAMP_NTZ(9),
        NEW_REPEAT_USS VARCHAR(16777216),
        SWIFT_TXN_ORDER_ID VARCHAR(16777216),
        CATALOG_REF_ID VARCHAR(16777216),
        EXTERNAL_ORDER_ID VARCHAR(16777216),
        DELETED_AT_IST TIMESTAMP_NTZ(9),
        INVOICE_DETAILS VARCHAR(16777216),
        PAYMENT_INFO VARCHAR(16777216),
        ORDER_COMPLETION_TIME_SEC NUMBER(18,0),
        ORDER_COMPLETION_TIME_MINS NUMBER(18,0),
        ORDER_COMPLETION_TIME_HOUR NUMBER(9,0),
        ORDER_COMPLETION_TIME_DAYS NUMBER(9,0),
        PREV_CREATED_AT_IST TIMESTAMP_NTZ(9),
        DAYS_SINCE_PREV_INVESTED NUMBER(9,0)
    
);

COMMENT ON TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS IS 'This is the US Stocks transaction table which has very deep data about the US Stocks transactions table which has knowledge about Buy/ Sell orders, the amount of time it took for order completion, the stock where the order was placed, the information & invoice details of the payment, the workflow related details of the order and much more';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TABLE_REFRESH_TIME IS '{"comment":"It is the time at which the table is refreshed. This not a very important field & can be ignore for most queries"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ACTOR_ID IS '{ "comment": "It is the identifier for a user across the organisation. This is a data point present across most tables in the organisation where there is a user action. Should be used as a joining key, since it represents the user identifier.","examples": ["35479187-1a5a-4dd2-80fd-695c2eb3f657","20188659-94f0-46b2-bfb8-a3bdb3605f0d","7b62cbda-a73f-4768-aa42-deced1ceaf5e"]}'
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_ID IS '{"comment":"It is the identifier for a US Stocks Buy or sell transaction. This is the primary key of this table and will remain unique. This is typically used for mosr of our developer debugging use-cases","examples": ["USSOusxpKagKfr240618","USSO48S8CJYuLE240618","USSO2ii2jnEdL7240718"]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.CLIENT_ORDER_ID IS  '{"comment":"Client order ID is the order ID which is sometimes used for debugging anything on Android or iOS clients. It is also a primary key and will remain unique","examples":["1b8a9688-2b62-4718-9b2a-ffd786562669","715ce3d2-7bb0-4a72-babc-76342751bb32"]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.VENDOR_ORDER_ID IS  '{"comment":"Vendor order ID is the order ID which is used for debugging orders with the downstream vendor. It is also a primary key and will remain unique"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.VENDOR_ACCOUNT_ID IS  '{"comment":"This is unique identifier for a US Stocks brokerage account which is opened with the vendor. Typically used for debugging with the vendor"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.POOL_TXN_ORDER_ID IS '{"comment":"This column can be ignore for this table"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WF_REQ_ID IS '{"comment":"This is a column often used for debugging by engineering team and checking the status of the workflows running behind the order. This is also a priamry key for this table"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TYPE IS '{"comment":"Type describes whether the order is a Buy order or Sell order","examples":[{"value":"BUY","explanation":"For when there is a buy order"},{"value":"SELL","explanation":"For when there is a sell order"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_STATUS IS '{"comment":"Status describes the status of the order","examples":[{"value":"ORDER_CANCELED","explanation":"When a buy or sell order is placed & then canceled by the user"},{"value":"ORDER_SUCCESS","explanation":"For when an order is fulfilled by vendor broker successfully"},{"value":"ORDER_INITIATION_FAILED","explanation":"For when order initiation with the vendor itself fails. This typically happens if there is a bug or a technical issue because orders dont get placed with vendor"},{"value":"ORDER_FAILED","explanation":"For when order gets placed but the order fails"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_TIME_IST IS '{"comment":"Time in IST when the order was placed by the user", "examples":"2024-06-18T20:58:38.156Z"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_UPDATED_TIME_IST IS '{"comment":"Time in IST when the order was most recently updated", "examples":"2024-06-18T21:15:26.473Z"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_DATE IS '{"comment":"Date in IST when the order was placed by the user. This is used to aggregate over day. This is the most commonly used column for aggregating orders over a day", "examples":"2024-06-18"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_UPDATED_DATE IS '{"comment":"Date in IST when the order was most recently updated. This is used to aggregate over day", "examples":"2024-06-18"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_WEEK IS '{"comment":"Date week in IST when the order was placed by the user. This is used to aggregate over week. This is the most commonly used column for aggregating orders over a week", "examples":"2024-06-18"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_MONTH IS '{"comment":"Date month in IST when the order was placed by the user. This is used to aggregate over a month. This is the most commonly used column for aggregating orders over a month", "examples":"2024-06-01"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_AMOUNT_REQUESTED_USD IS '{"comment":"This is the transaction amount in USD currency for which the order was placed. This is typically the column that should be referred to when checking for the order amount", "examples":"1.000000"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_AMOUNT_CONFIRMED_USD IS '{"comment":"This is the transaction amount in USD currency for which the order was confirmed and fulfilled. This is usually the same as TXN_AMOUNT_REQUESTED", "examples":"1.000000"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.QTY_REQUESTED IS '{"comment":"This is the quantity of the stock for which the order is requested.", "examples":"0.00649645943"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.QTY_CONFIRMED IS '{"comment":"This is the quantity of the stock for which the order is confirmed. The value of it will be 0 for when the order status is not successful", "examples":"0.012829128"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_PRICE_AT_REQUESTED_USD IS '{"comment":"This is the price of the stock in USD when the US Stock order was placed","examples":"32.64"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_PRICE_AT_CONFIRMED_USD IS '{"comment":"This is the price of the stock in USD when the US Stock order was confirmed. The value of it will be 0 for when the order status is not successful","examples":"32.64"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_SYMBOL IS '{"comment":"Describes the ticker/ symbol of the stock on the stock market","examples":[{"value":"MSFT","explanation":"MSFT is the symbol for Microsoft"},{"value":"TSLA","explanation":"TSLA is the symbol for Tesla"},{"value":"NVDA","explanation":"NVDA is the symbol for Nvidia"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_ID IS '{"comment":"This is the unique identifier of a particular ticker/ stock in the organisations tables","examples":"USS221228gbUTWdXyTEawkWJlQA+4qg=="}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_EXCHANGE IS '{"comment":"This is the unique identifier of the exchange where the stock is listed on","examples":[{"value":"EXCHANGE_NAS","explanation":"For NASDAQ"},{"value":"EXCHANGE_ASE","explanation":"For American Stock Exchange"},{"value":"EXCHANGE_ARCA","explanation":"For Arca Stock Exchange, mostly ETFs listed here"},{"value":"EXCHANGE_NYSE","explanation":"For New York Stock Exchange"},{"value":"EXCHANGE_BATS","explanation":"For BATS Stock Exchange, mostly ETFs listed here"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_INTERNAL_STATUS IS '{"comment":"Internal status defines whether the stock is active or disabled for buy.","examples":[{"value":"INTERNAL_STATUS_DISABLED_BUY","explanation":"When the stock is disabled for buy"},{"value":"INTERNAL_STATUS_AVAILABLE","explanation":"When the stock is available for buy"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.MARKET_CATEGORY_NAME IS '{"comment":"This defines the industry/ market category to which the stock for which the order is placed belongs.","examples":[{"value":"Healthcare Plans"},{"value":"Uranium"},{"value":"Building Materials"},{"value":"Broadcasting"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_COMPANY_NAME IS '{"comment":"This defines the name of the company associated with the stock.","examples":[{"value":"Occidental Petroleum Corp"},{"value":"GitLab Inc"},{"value":"Autodesk Inc"},{"value":"LivePerson Inc"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_INDUSTRY_ID IS '{"comment":"This defines the indsutry ID of the stock. It is an attirbute of a stock"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_INDUSTRY_GROUP_ID IS '{"comment":"This defines the indsutry group ID of the stock. It is an attirbute of a stock"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_SECTOR_ID IS '{"comment":"This defines the sector ID of the stock. It is an attribute of a stock"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_STAGE IS '{"comment":"Each of the orders will be associated with a workflow which is running in the background. This defines the stage at which the workflow is at Column is to be used when workflow specific information is required.","examples":[{"value":"TRACK_ORDER","explanation":"This is after the users order is placed whether it has been confirmed by the vendor broker"},{"value":"SEND_SELL_ORDER","explanation":"This is used for tracking whether the users sell order is placed"},{"value":"SEND_BUY_ORDER","explanation":"This is used for tracking whether the users buy order is placed"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_STATUS IS '{"comment":"Each of the orders will be associated with a workflow which is running in the background. The workflow has various stages defined in WORKFLOW_STAGE column. This defines the status of the stage of the workflow.","examples":[{"value":"MANUAL_INTERVENTION","explanation":"When some error happens, a workflow goes into manual intervention for the engineer to fix manually"},{"value":"SUCCESSFUL","explanation":"Everything happened as expected"},{"value":"CANCELED","explanation":"Some user intervention happened to cancel the workflow"},{"value":"FAILED","explanation":"Some error occurred which is a terminal error"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_VERSION IS '{"comment":"This defines version of the workflow","examples":"v0"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_TYPE IS '{"comment":"This defines the workflow type, which can be a Buy transaction, Sell transaction, or a reward transaction.","examples":[{"value":"BUY_TRANSACTION","explanation":"Represents a Buy transaction workflow"},{"value":"SELL_TRANSACTION","explanation":"Represents a Sell transaction workflow"},{"value":"REWARD_TRANSACTION","explanation":"Represents a reward transaction workflow. We should use this value when there are any stock reward related queries"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ACCOUNT_ID IS '{"comment":"This defines the account ID that we have defined internally for a users vendor broker account."}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ACCOUNT_CREATED_TIME_IST IS '{"comment":"This defines the time at which the users vendor broker account is create in IST (indian standard time)"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.DAYS_SINCE_ACCOUNT_CREATION IS '{"comment":"This tells how many days it has been since the user has created the account"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.FIRST_INVEST_TIME_IST IS '{"comment":"This tells the time in IST when a user invests in US Stocks for the first time during their lifetime","examples":"2024-06-18T20:58:38.156Z"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.NEW_REPEAT_USS IS '{"comment":"This tells whether for that order, the user has invested for the first time in their lifetime or they are a repeat user","examples":[{"value":"Repeat"},{"value":"New"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.EXTERNAL_ORDER_ID IS '{"comment":"This tells the order ID which is visible to the end user on their invoice. Hence the ID is used when there is a user issue on a specific order"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.ORDER_COMPLETION_TIME_SEC IS '{"comment":"This tells in seconds how much time it took for the order to get fulfilled from order placement time"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.ORDER_COMPLETION_TIME_MINS IS '{"comment":"This tells in minutes how much time it took for the order to get fulfilled from order placement time"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.ORDER_COMPLETION_TIME_HOUR IS '{"comment":"This tells in hours how much time it took for the order to get fulfilled from order placement time"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.ORDER_COMPLETION_TIME_DAYS IS '{"comment":"This tells in days how much time it took for the order to get fulfilled from order placement time"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.PREV_CREATED_AT_IST IS '{"comment":"This tells the timestamp of the previous successful order placed by the user if the user has placed a order before this"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.DAYS_SINCE_PREV_INVESTED IS '{"comment":"This tells the number days since the previous successful order placed by the user if the user has placed a order before this"}';
"""
)

vn.train(
    ddl="""
create or replace TRANSIENT TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT (
        TABLE_REFRESH_TIME TIMESTAMP_LTZ(9),
        ACTOR_ID VARCHAR(16777216),
        ACCOUNT_ID VARCHAR(16777216),
        ACCOUNT_STATUS VARCHAR(16777216),
        VENDOR_ACCOUNT_ID VARCHAR(16777216),
        EXTERNAL_ACCOUNT_ID VARCHAR(16777216),
        ACCT_CREATION_WF_REQ_ID VARCHAR(16777216),
        ACCT_ROW_DELETED_AT_IST TIMESTAMP_NTZ(9),
        SUITABILITY_STEP_CREATED_AT_IST TIMESTAMP_NTZ(9),
        SUITABILITY_STEP_UPDATED_AT_IST TIMESTAMP_NTZ(9),
        DATE_OF_BIRTH DATE,
        SUITABILITY_FORM_RISK_LEVEL_OPTED VARCHAR(16777216),
        SUITABILITY_FORM_ITR_ENQUIRY VARCHAR(16777216),
        SUITABILITY_FORM_EMPLOYMENT_TYPE VARCHAR(16777216),
        SUITABILITY_FORM_INCOME_RANGE VARCHAR(16777216),
        SUITABILITY_FORM_INVESTED_INST VARIANT,
        SUITABILITY_FORM_EDUCATION_QUALIFICATION VARCHAR(16777216),
        SUITABILITY_FORM_EXPECTED_AMOUNT_TO_INVEST VARCHAR(16777216),
        DATE_OF_BIRTH_UNPARSED VARCHAR(16777216),
        SUITABILITY_SCORE NUMBER(38,0),
        REMITTANCE_LIMIT_INR NUMBER(38,0),
        SUITABILITY_STATUS VARCHAR(16777216),
        ACCT_CREATION_TIME_IST TIMESTAMP_NTZ(9),
        ACCT_CREATION_DATE_IST DATE,
        ACCT_CREATION_WEEK_IST DATE,
        ACCT_CREATION_MONTH_IST DATE,
        ACCT_CREATION_WORKFLOW_ID VARCHAR(16777216),
        ACCT_CREATION_WORKFLOW_STAGE VARCHAR(16777216),
        ACCT_CREATION_WORKFLOW_STATUS VARCHAR(16777216),
        ACCT_CREATION_WORKFLOW_VERSION VARCHAR(16777216),
        ACCT_CREATION_WORKFLOW_TYPE VARCHAR(16777216),
        CLIENT_REQ_ID VARCHAR(16777216),
        ACCT_CREATION_START_TIME_IST TIMESTAMP_NTZ(9),
        ACCT_CREATION_TIME_MINS NUMBER(18,0),
        ACCT_CREATION_TIME_HOUR NUMBER(9,0),
        ACCT_CREATION_TIME_DAYS NUMBER(9,0),
        DAYS_SINCE_ACCOUNT_CREATED NUMBER(9,0),
        TOTAL_WALLET_FUNDS_ADDED_USD FLOAT,
        TOTAL_WALLET_FUNDS_WITHDRAW_USD FLOAT,
        NUM_SUCCESS_ADD_FUND_TXNS NUMBER(18,0),
        NUM_SUCCESS_WALLET_WITHDRAW_FUND_TXNS NUMBER(18,0),
        NUM_SUCCESS_WALLET_TXNS NUMBER(18,0),
        FIRST_SUCCESS_ADD_FUND_DATE DATE,
        FIRST_SUCCESS_ADD_FUND_TIME TIMESTAMP_NTZ(9),
        FIRST_SUCCESS_ADD_FUND_AMT_USD FLOAT,
        FIRST_SUCCESS_WITHDRAW_FUND_DATE DATE,
        FIRST_SUCCESS_WITHDRAW_FUND_TIME TIMESTAMP_NTZ(9),
        FIRST_SUCCESS_WITHDRAW_FUND_AMT_USD FLOAT,
        LAST_SUCCESS_ADD_FUND_DATE DATE,
        LAST_SUCCESS_ADD_FUND_TIME TIMESTAMP_NTZ(9),
        LAST_SUCCESS_ADD_FUND_AMT_USD FLOAT,
        LAST_SUCCESS_WITHDRAW_FUND_DATE DATE,
        LAST_SUCCESS_WITHDRAW_FUND_TIME TIMESTAMP_NTZ(9),
        LAST_SUCCESS_WITHDRAW_FUND_AMT_USD FLOAT,
        AUM_USD FLOAT,
        AUM_USD_BUCKET VARCHAR(16777216),
        ACCOUNT_CLOSED_TIME_IST TIMESTAMP_NTZ(9),
        ACCOUNT_CLOSED_DATE DATE,
        NUM_ORDERS NUMBER(18,0),
        NUM_SUCCESS_ORDERS NUMBER(18,0),
        NUM_SUCCESS_BUY_ORDERS NUMBER(18,0),
        NUM_SUCCESS_SELL_ORDERS NUMBER(18,0),
        TOTAL_BUY_AMOUNT_USD NUMBER(38,6),
        TOTAL_SELL_AMOUNT_USD NUMBER(38,6),
        DISTINCT_STOCKS_BOUGHT NUMBER(18,0),
        DISTINCT_STOCKS_SOLD NUMBER(18,0),
        FIRST_ORDER_DATE DATE,
        FIRST_ORDER_WEEK DATE,
        FIRST_ORDER_MONTH DATE,
        LAST_ORDER_DATE DATE,
        LAST_ORDER_WEEK DATE,
        LAST_ORDER_MONTH DATE,
        FIRST_BUY_AMOUNT_USD NUMBER(38,6),
        FIRST_BUY_QTY FLOAT,
        FIRST_BUY_STOCK VARCHAR(16777216),
        FIRST_BUY_DATE DATE,
        FIRST_SELL_AMOUNT_USD NUMBER(38,6),
        FIRST_SELL_QTY FLOAT,
        FIRST_SELL_STOCK VARCHAR(16777216),
        FIRST_SELL_DATE DATE,
        LAST_BUY_AMOUNT_USD NUMBER(38,6),
        LAST_BUY_QTY FLOAT,
        LAST_BUY_STOCK VARCHAR(16777216),
        LAST_BUY_DATE DATE,
        LAST_SELL_AMOUNT_USD NUMBER(38,6),
        LAST_SELL_QTY FLOAT,
        LAST_SELL_STOCK VARCHAR(16777216),
        LAST_SELL_DATE DATE,
        DISTINCT_STOCKS_BOUGHT_EVER VARCHAR(16777216),
        DAYS_SINCE_FIRST_ORDER NUMBER(9,0),
        DAYS_SINCE_FIRST_BUY_ORDER NUMBER(9,0),
        DAYS_SINCE_FIRST_SELL_ORDER NUMBER(9,0),
        DAYS_SINCE_LAST_ORDER NUMBER(9,0),
        DAYS_SINCE_LAST_BUY_ORDER NUMBER(9,0),
        DAYS_SINCE_LAST_SELL_ORDER NUMBER(9,0),
        DISTINCT_STOCKS_WATCHLISTED_CURRENT VARCHAR(16777216),
        NUM_DISTINCT_STOCKS_WATCHLISTED_CURRENT NUMBER(18,0),
        DISTINCT_STOCKS_VISITED VARCHAR(16777216),
        NUM_DISTINCT_STOCKS_VISITED NUMBER(18,0),
        EVER_SEARCHED NUMBER(1,0),
        HAS_WATCHLISTED_CURRENT NUMBER(1,0),
        EVER_VISITED_STOCK NUMBER(1,0),
        EVER_PURCHASED_STOCK NUMBER(1,0)
);

COMMENT ON TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT IS 'This is a user level table which has detailed information about the account, accuont creation time, step in account creation, how much funds are added, withdrawn, how much stocks were bought, which stocks were bought, what stocks are watchlisted, visited, when they were bought, when the first add funds were done and much more. This essentially can be a really good first source of truth for several queries because of the extent and the number of columns available here';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TABLE_REFRESH_TIME IS '{"comment":"It is the time at which the table is refreshed. This not a very important field & can be ignore for most queries"}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACTOR_ID IS '{ "comment": "It is the identifier for a user across the organisation. This is a data point present across most tables in the organisation where there is a user action. Should be used as a joining key, since it represents the user identifier.","examples": ["35479187-1a5a-4dd2-80fd-695c2eb3f657","20188659-94f0-46b2-bfb8-a3bdb3605f0d","7b62cbda-a73f-4768-aa42-deced1ceaf5e"]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCOUNT_STATUS IS '{"comment":"Describes the status of the US Stocks Account. Typically this column is used only to check whether the account creation is done or not. Account creation is done when the status is \"ACTIVE\". In rest of all cases, the account creation is not done regardless of the status.", "examples":[{"value":"MANUAL_INTERVENTION","explanation":"This means that the account creation is stuck because of some technical issue and is waiting for developer intervention to make it reach a terminal state"},{"value":"INITIATED", "explanation":"When the account creation has started at the broker. It is not active yet."},{"value":"KYC_VERIFIED","explanation":"It means the account is not active yet."},{"value":"CREATION_ON_HOLD","explanation":"It means the account is not active yet."},{"value":"ACTIVE","explanation":"It means the account is active"},{"value":"ACCOUNT_STATUS_UNSPECIFIED","explanation":"It means the account is not active yet"},{"value":"CREATED","explanation":"It means the account is created but not active yet"}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.VENDOR_ACCOUNT_ID IS '{"comment":"This is unique identifier for a US Stocks brokerage account which is opened with the vendor. Typically used for debugging with the vendor. For any vendor use cases, vendor account ID can be used."}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EXTERNAL_ACCOUNT_ID IS '{"comment": "This ID is different from both ACCOUNT_ID and VENDOR_ACCOUNT_ID. It is a user-friendly identifier intended for display to the user. It is not typically used for queries."}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WF_REQ_ID IS '{"comment": "WF stands for Workflow. For each account creation attempt, a unique workflow is created at the backend. This ID identifies that specific workflow and can be used for debugging purposes."}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_STEP_CREATED_AT_IST IS '{"comment": "This timestamp indicates when a user begins the US stocks suitability assessment, which is the first step in the US stocks account creation process."}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_STEP_UPDATED_AT_IST IS '{"comment": "This timestamp indicates when the US stocks suitability data is updated. Not frequently used."}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DATE_OF_BIRTH IS '{"comment": "This is the user\'s actual date of birth."}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_RISK_LEVEL_OPTED IS '{"comment": "This is the risk level the user opted for in the US Stocks suitability form. It indicates their willingness to take risks in investments.", "examples":[{"value": "low-risk", "explanation": "User prefers investments with lower potential returns but also lower potential losses."}, {"value": "medium-risk", "explanation": "User is comfortable with a moderate level of risk for the potential of moderate returns."}, {"value": "high-risk", "explanation": "User is willing to accept higher risks for the possibility of higher returns."}]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_ITR_ENQUIRY IS '{"comment": "This column indicates whether the user has filed an Income Tax Return (ITR) in the last 2 years, as part of the US Stocks suitability assessment.", "examples":[{"value": "no-itr-filed-2-year", "explanation": "User has not filed an ITR in the last 2 years."}, {"value": "yes-itr-filed-2-year", "explanation": "User has filed an ITR in the last 2 years."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_EMPLOYMENT_TYPE IS '{"comment": "This column indicates the user\'s employment type, as declared during the US Stocks suitability assessment.", "examples":[{"value": "homemaker-employment", "explanation": "User identifies as a homemaker."}, {"value": "business-owner-professional-employment", "explanation": "User is a business owner or professional."}, {"value": "others-employment", "explanation": "User selected 'Other' for employment type."}, {"value": "salaried-with-less-than-6-months-experience-employment", "explanation": "User is a salaried employee with less than 6 months of experience."}, {"value": "working-professional-employment", "explanation": "User is a working professional."}, {"value": "retired-employment", "explanation": "User is retired."}, {"value": "student-employment", "explanation": "User is a student."}, {"value": "self-employed-or-freelancer-employment", "explanation": "User is self-employed or a freelancer."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_INCOME_RANGE IS '{"comment": "This column represents the user\'s self-reported income range, selected from predefined brackets, as part of the US Stocks suitability assessment.", "examples": ["100000-500000", "2500000-10000000", "1000000-2500000", "500000-1000000", "10000000-25000000", "2500000-5000000", "5000000-10000000", "10000000-1000000000"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_INVESTED_INST IS '{"comment": "This column stores a JSON array of the user\'s invested instruments, as declared in the US Stocks suitability assessment.  The array represents the different types of investments the user currently holds. To query specific instruments within the array, JSON parsing will be required.", "examples": [
  "[\"other-debtmf-sgbs-reits-investment\", \"overseas-investments-investment\", \"stock-equity-mutual-fund-investment\", \"physical-gold-real-state-investment\"]",
  "[\"fixed-recurring-deposit-investment\", \"stock-equity-mutual-fund-investment\", \"overseas-investments-investment\", \"physical-gold-real-state-investment\", \"other-debtmf-sgbs-reits-investment\"]",
  "[\"stock-equity-mutual-fund-investment\", \"other-debtmf-sgbs-reits-investment\", \"fixed-recurring-deposit-investment\", \"overseas-investments-investment\", \"physical-gold-real-state-investment\"]"
]}';
COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_EDUCATION_QUALIFICATION IS '{"comment": "This column indicates the user\'s highest level of education, as declared during the US Stocks suitability assessment.", "examples":[{"value":"high-school-education-qualification", "explanation":"User has completed high school."}, {"value":"graduate-education-qualification", "explanation":"User has earned a bachelor's degree."}, {"value":"post-graduate-education-qualification", "explanation":"User has a master's degree or equivalent."}, {"value":"professional-degree-education-qualification", "explanation":"User holds a professional degree (e.g., MBA, JD, MD)."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_EXPECTED_AMOUNT_TO_INVEST IS '{"comment": "This column describes the user\'s expected investment amount in US Stocks, using predefined text ranges.", "examples": ["morethan-10k-lessthan-50k-expected-uss-investment", "morethan-1L-lessthan-5L-expected-uss-investment", "morethan-50k-lessthan-1L-expected-uss-investment", "lessthan-10K-expected-uss-investment", "morethan-5lakh-expected-uss-investment"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_SCORE IS '{"comment": "This score, ranging from 0-50, is generated based on the user\'s responses in the suitability assessment. A higher score indicates a greater suitability for investing in US Stocks. Factors influencing the score include income level, risk tolerance, and investment experience. For example, users with higher incomes, a greater willingness to take risks, and more investment experience are likely to have higher suitability scores."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.REMITTANCE_LIMIT_INR IS '{"comment": "This is the maximum amount, in Indian Rupees (INR), that a user can invest in US Stocks within a financial year (April to March). This limit is a regulatory requirement set by our organization on international remittance allowed for US Stocks. In case this is 0 or null, user is not allowed to make international remittances"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_STATUS IS '{"comment": "This column indicates the user\'s current stage in the US Stocks suitability assessment process.", "examples":[{"value":"SUITABILITY_STATUS_SCORE_CALCULATED", "explanation":"The user\'s suitability score has been calculated, and they are eligible to proceed."}, {"value":"SUITABILITY_STATUS_PROFILE_DATA_COLLECTED", "explanation":"The collection of suitability profile data is complete."}, {"value":"SUITABILITY_STATUS_USER_INELIGIBLE", "explanation":"The user is ineligible for international transactions."}, {"value":"SUITABILITY_STATUS_INITIATED", "explanation":"The suitability data collection process has been initiated."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_IST IS '{"comment": "This timestamp indicates when the user\'s US Stocks account was successfully created. It will be NULL if the account creation was not successful or has not yet occurred."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_DATE_IST IS '{"comment": "This column represents the date on which the user\'s US Stocks account was successfully created. It is derived from ACCT_CREATION_TIME_IST and is useful for aggregations where the specific time of day is not required."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WEEK_IST IS '{"comment": "This column represents the start date (Monday) of the week in which the user\'s US Stocks account was successfully created. It is used for weekly aggregations."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_MONTH_IST IS '{"comment": "This column represents the first day of the month in which the user\'s US Stocks account was successfully created. It is used for monthly aggregations."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WORKFLOW_STAGE IS '{"comment": "This column indicates the specific stage of the account creation workflow where the user is currently at. It provides a more detailed breakdown of the progress compared to ACCOUNT_STATUS.", "examples": [{"value": "US_BROKER_ACCOUNT_OPENING_COLLECT_AGREEMENTS", "explanation": "The account opening workflow is at the stage where it requests the user to agree to some agreements."}, {"value": "US_BROKER_ACCOUNT_OPENING_MANUAL_PAN_REVIEW", "explanation": "The account opening workflow is at a stage where the user goes into a manual PAN review which is done by manually by operations team at the back end."}, {"value": "US_BROKER_ACCOUNT_OPENING_COLLECT_SOURCE_OF_FUNDS", "explanation": "This represents the step when the users source of funds document is being collected."}, {"value": "US_BROKER_ACCOUNT_OPENING_MANUAL_PAN_UPLOAD", "explanation": "This represents the step when user is manually uploading their PAN in the account onboarding flow."}, {"value": "US_BROKER_ACCOUNT_OPENING_COLLECT_POA_AND_POI", "explanation": "This represent the step when user is giving consent to collection their Proof of address & proof of identity, in case it is already available in our database."}, {"value": "USS_ACCOUNT_CREATION_ON_HOLD", "explanation": "This stage represents when even if user completes all steps, their account could not be created because it doesnt meet one or other reason for not creating account e.g. PAN uploaded was faulty, some required data is not available etc."}, {"value": "US_BROKER_ACCOUNT_OPENING_UPLOAD_KYC_DATA", "explanation": "This stage represents a backend step in the entire workflow and is typically an automated process to move ahead from this stage without user input."}, {"value": "US_BROKER_ACCOUNT_OPENING_COLLECT_RISK_DISCLOSURE", "explanation": "This stage represents a screen where we ask the users for a risk disclosure in case we feel a user may be risky."}, {"value": "US_BROKER_ACCOUNT_OPENING_COLLECT_EMPLOYMENT_DETAILS", "explanation": "This stage represents the employment details collection stage of the workflow."}, {"value": "US_BROKER_ACCOUNT_OPENING_ACCOUNT_OPENING_WITH_VENDOR", "explanation": "This stage represents when the account opening with broker is being done. This should be an automated process."}, {"value": "US_BROKER_ACCOUNT_OPENING_AML_CHECK", "explanation": "This stage represents an Anti money laundering check that is done at the back end before requesting an account opening."}, {"value": "US_BROKER_ACCOUNT_OPENING_WAIT_FOR_DOCUMENTS_UPLOAD", "explanation": "This stage is a backend step which waits for users documents to get uploaded."}, {"value": "US_BROKER_ACCOUNT_OPENING_POLL_ACCOUNT_STATUS", "explanation": "This stage is when the backend polls the vendor broker on what exactly the account opening status is."}, {"value": "US_BROKER_ACCOUNT_OPENING_FETCH_ADDRESS", "explanation": "This stage is a backend process when the users address is being fetched from their account statement."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WORKFLOW_VERSION IS '{"comment":"This column indicates the specific version of the account creation workflow that the user went through. Different versions of the workflow may have been used over time due to product updates or changes.", "examples":[{"value":"V1", "explanation":"User went through version 1 of the workflow."}, {"value":"V0", "explanation":"User went through version 0 of the workflow."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_START_TIME_IST IS '{"comment": "This timestamp indicates precisely when the user initiated the US Stocks account creation process, marking their entry into the first stage of the workflow.", "examples": "2024-07-16T09:07:22.425Z"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_MINS IS '{"comment": "This column records the total time taken, in minutes, to complete the US Stocks account creation process. It measures the duration from the users first step in the workflow to the final stage.  Importantly, this value will be NULL if the account is not yet active, indicating that the creation process is still ongoing."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_HOUR IS '{"comment": "This column records the total time taken, in hours, to complete the US Stocks account creation process. It measures the duration from the users first step in the workflow to the final stage.  This value will be NULL if the account is not yet active."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_DAYS IS '{"comment": "This column records the total time taken, in days, to complete the US Stocks account creation process. It measures the duration from the users first step in the workflow to the final stage.  The value will be NULL if the account is not yet active."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_ACCOUNT_CREATED IS '{"comment": "This column indicates the number of days that have elapsed since the users US Stocks account was successfully created.  It provides a measure of account age."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_WALLET_FUNDS_ADDED_USD IS '{"comment":"This represents how much funds in USD the user has added to their US Broker wallet account since when they opened the account.","examples":["1000.00","5000.00","200.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_WALLET_FUNDS_WITHDRAW_USD IS '{"comment":"This represents how much money the user has withdrawn from their USD wallet over lifetime."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_ADD_FUND_TXNS IS '{"comment":"This is the number of successful add funds transactions that user has done over lifetime."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_WALLET_WITHDRAW_FUND_TXNS IS '{"comment":"This is the number of successful withdraw transactions user has done since they created their account."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_WALLET_TXNS IS '{"comment":"This represents how many successful wallet transactions the user has done in their lifetime.","examples":"5"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_ADD_FUND_DATE IS '{"comment":"This represents the date on which the user first added funds after account creation in their lifetime. This is an important column.","examples":"2024-06-18"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_ADD_FUND_TIME IS '{"comment":"This represents the time on which the user first added funds after account creation in their lifetime. This is an important column.","examples":"2024-06-18T20:58:38.156Z"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_ADD_FUND_AMT_USD IS '{"comment":"This represents the amount in USD of the first successful add funds transaction. This is an important column."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_WITHDRAW_FUND_DATE IS '{"comment":"This represents the date on which the user first withdrew funds after account creation in their lifetime. This is an important column.","examples":"2024-06-18"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_WITHDRAW_FUND_TIME IS '{"comment":"This represents the time on which the user first withdrew funds after account creation in their lifetime. This is an important column.","examples":"2024-06-18T20:58:38.156Z"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_WITHDRAW_FUND_AMT_USD IS '{"comment":"This represents the amount in USD of the first successful withdraw funds transaction. This is an important column.","examples":"13.50"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_ADD_FUND_DATE IS '{"comment":"This represents the date on which the user has done their last successful add funds to wallet transaction.","examples":"2024-06-18"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_ADD_FUND_TIME IS '{"comment":"This represents the time on which the user has done their last successful add funds to wallet transaction.","examples":"2024-06-18T20:58:38.156Z"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_ADD_FUND_AMT_USD IS '{"comment":"This represents the amount in USD of the last successful add funds to wallet transaction.","examples":"12.60"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_WITHDRAW_FUND_DATE IS '{"comment":"This represents the date on which the user has done their last successful withdraw funds from wallet transaction.","examples":"2024-06-18"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_WITHDRAW_FUND_TIME IS '{"comment":"This represents the time on which the user has done their last successful withdraw funds from wallet transaction.","examples":"2024-06-18T20:58:38.156Z"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_WITHDRAW_FUND_AMT_USD IS '{"comment":"This represents the amount in USD of the last successful withdraw funds from wallet transaction."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.AUM_USD IS '{"comment":"This represents the assets under management in USD that we have for the user.","examples":"1208.40"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.AUM_USD_BUCKET IS '{"comment":"This column has the bucket of amounts in USD.","examples":[{"value":">2K USD","explanation":"More than 2000 USD"},{"value":"1K-2K USD","explanation":"Between 1000 USD and 2000 USD"},{"value":"500-1K USD","explanation":"Between 500 USD and 1000 USD"},{"value":"<10 USD","explanation":"Less than 10 USD"},{"value":"10-100 USD","explanation":"Between 10 USD and 100 USD"},{"value":"100-500 USD","explanation":"Between 100 USD and 500 USD"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_ORDERS IS '{"comment":"This represents the number of stock buy or sell order attempts. This excludes any add funds or withdraw funds wallet orders and includes only buy or sell order attempts regardless of whether they are successful or failed."';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_ORDERS IS '{"comment":"This represents the number of successful stock buy or sell orders. This excludes any add funds or withdraw funds wallet orders and includes only buy or sell orders which got fulfilled successfully."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_BUY_ORDERS IS '{"comment":"This represents the number of successful stock buy orders. This excludes any add funds or withdraw funds wallet orders and includes only buy orders which got fulfilled successfully."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_SELL_ORDERS IS '{"comment":"This represents the number of successful stock sell orders. This excludes any add funds or withdraw funds wallet orders and includes only sell orders which got fulfilled successfully."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_BUY_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of successful stock buy orders. It doesnt take into account orders which are still in progress or failed."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_SELL_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of successful stock sell orders. It doesnt take into account orders which are still in progress or failed."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_BOUGHT IS '{"comment":"This represents the number of distinct stock symbols or stocks that the user has bought. If the user has bought Microsoft and Google stocks in the portfolio, then the number of distinct stocks is 2.",}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_SOLD IS '{"comment":"This represents the number of distinct stock symbols or stocks that the user has sold."}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_ORDER_DATE IS '{"comment":"This represents the date on which the first buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_ORDER_WEEK IS '{"comment":"This represents the week on which the first buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for week based aggregations","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_ORDER_MONTH IS '{"comment":"This represents the month on which the first buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for month based aggregations","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_ORDER_DATE IS '{"comment":"This represents the date on which the last buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_ORDER_WEEK IS '{"comment":"This represents the week on which the last buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for week based aggregations","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_ORDER_MONTH IS '{"comment":"This represents the month on which the last buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for month based aggregations","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_AMOUNT_USD IS '{"comment":"This represents the amount in USD for the first buy order that the user placed.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_QTY IS '{"comment":"This represents the quantity of stocks that the user bought in their first every buy order on stocks","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_STOCK IS '{"comment":"This is the symbol of the stock which the user bought first in their lifetime.","examples":[{"value":"MSFT","explanation":"Microsoft"},{"value":"INTC","explanation":"Intel"},{"value":"ADCT","explanation":"ADC Telecommunications"},{"value":"CVX","explanation":"Chevron"},{"value":"VNET","explanation":"22VNET Group"},{"value":"CGAU","explanation":"China Gas Holdings"},{"value":"ONON","explanation":"Onconova Therapeutics"},{"value":"GLW","explanation":"Corning"},{"value":"BLDR","explanation":"Builders FirstSource"},{"value":"CRM","explanation":"Salesforce"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_DATE IS '{"comment":"This is the date on which the first buy order was placed by the user.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_AMOUNT_USD IS '{"comment":"This represents the amount in USD for the first sell transaction that the user did.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_QTY IS '{"comment":"This is the quantity of stock which the user sold in the first ever sell transaction","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_STOCK IS '{"comment":"This is the symbol of the stock which the user sold first in their lifetime.","examples":[{"value":"MSFT","explanation":"Microsoft"},{"value":"INTC","explanation":"Intel"},{"value":"ADCT","explanation":"ADC Telecommunications"},{"value":"CVX","explanation":"Chevron"},{"value":"VNET","explanation":"22VNET Group"},{"value":"CGAU","explanation":"China Gas Holdings"},{"value":"ONON","explanation":"Onconova Therapeutics"},{"value":"GLW","explanation":"Corning"},{"value":"BLDR","explanation":"Builders FirstSource"},{"value":"CRM","explanation":"Salesforce"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_DATE IS '{"comment":"This is the date on which the user placed their first ever sell transaction.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_AMOUNT_USD IS '{"comment":"This represents the amount in USD for the last buy order that the user placed","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_QTY IS '{"comment":"This represents the quantity of stocks of the last buy order that the user placed","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_STOCK IS '{"comment":"This is the symbol of the stock which the user bought last in their lifetime.","examples":[{"value":"MSFT","explanation":"Microsoft"},{"value":"INTC","explanation":"Intel"},{"value":"ADCT","explanation":"ADC Telecommunications"},{"value":"CVX","explanation":"Chevron"},{"value":"VNET","explanation":"22VNET Group"},{"value":"CGAU","explanation":"China Gas Holdings"},{"value":"ONON","explanation":"Onconova Therapeutics"},{"value":"GLW","explanation":"Corning"},{"value":"BLDR","explanation":"Builders FirstSource"},{"value":"CRM","explanation":"Salesforce"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_DATE IS '{"comment":"The date on which the last buy order was placed by the user.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_AMOUNT_USD IS '{"comment":"This is the amount in USD of the last sell order the user has placed.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_QTY IS '{"comment":"This is the number of stocks which were sold by the user in their last sell order.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_STOCK IS '{"comment":"This is the symbol of the stock which the user sold last in their lifetime.","examples":[{"value":"MSFT","explanation":"Microsoft"},{"value":"INTC","explanation":"Intel"},{"value":"ADCT","explanation":"ADC Telecommunications"},{"value":"CVX","explanation":"Chevron"},{"value":"VNET","explanation":"22VNET Group"},{"value":"CGAU","explanation":"China Gas Holdings"},{"value":"ONON","explanation":"Onconova Therapeutics"},{"value":"GLW","explanation":"Corning"},{"value":"BLDR","explanation":"Builders FirstSource"},{"value":"CRM","explanation":"Salesforce"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_DATE IS '{"comment":"This is the date of the last sell transaction the user has ever placed.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_BOUGHT_EVER IS '{"comment":"This represents the number of distinct stocks the user has ever bought.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_FIRST_ORDER IS '{"comment":"This represents the number of days it has been since the user has placed their first buy or sell order.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_FIRST_BUY_ORDER IS '{"comment":"This represents the number of days it has been since the user has placed their first buy order.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_FIRST_SELL_ORDER IS '{"comment":"This represents the number of days it has been since the user has placed their first sell order.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_LAST_ORDER IS '{"comment":"This represents the number of days it has been since the user has placed their last buy or sell order.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_LAST_BUY_ORDER IS '{"comment":"This represents the number of days it has been since the user has placed their last buy order.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_LAST_SELL_ORDER IS '{"comment":"This represents the number of days it has been since the user has placed their last sell order.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_WATCHLISTED_CURRENT IS '{"comment":"This represents the list of stocks which are watchlisted by the user at present.","examples":[{"value":"NVDA","explanation":"User has NVDA in watchlist"},{"value":"AAPL, AXP, CVX, KHC, KO, MCO, OXY","explanation":"User has AAPL, AXP, CVX, KHC, KO, MCO, OXY in watchlist"},{"value":"BBY","explanation":"User has BBY in watchlist"},{"value":"AAPL, AMZN, MSFT, NVDA, UBER, WMT","explanation":"User has AAPL, AMZN, MSFT, NVDA, UBER, WMT in watchlist"},{"value":"GFI","explanation":"User has GFI in watchlist"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_DISTINCT_STOCKS_WATCHLISTED_CURRENT IS '{"comment":"This represents the number of stocks which are watchlisted by the user at present.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_VISITED IS '{"comment":"This represents the list of stocks which are visited by the user ever.","examples":[{"value":"NVDA","explanation":"User has visited NVDA"},{"value":"AAPL, AXP, CVX, KHC, KO, MCO, OXY","explanation":"User has visited AAPL, AXP, CVX, KHC, KO, MCO, OXY"},{"value":"BBY","explanation":"User has visited BBY"},{"value":"AAPL, AMZN, MSFT, NVDA, UBER, WMT","explanation":"User has visited AAPL, AMZN, MSFT, NVDA, UBER, WMT"},{"value":"GFI","explanation":"User has visited GFI"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_DISTINCT_STOCKS_VISITED IS '{"comment":"This represents the number of distinct stocks which are visited by the user ever.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EVER_SEARCHED IS '{"comment":"This indicates whether the user has ever used the search feature on US Stocks. It will be 1 if the user has searched, and will be null if the user has never searched","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.HAS_WATCHLISTED_CURRENT IS '{"comment":"This indicates whether the user has currently watchlisted any stocks.","examples":[{"value":"1","explanation":"User has watchlisted stocks"},{"value":"null","explanation":"User has not watchlisted any stocks"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EVER_VISITED_STOCK IS '{"comment":"This indicates whether the user has ever visited a stock page on US Stocks.","examples":[{"value":"1","explanation":"User has visited a stock page"},{"value":"null","explanation":"User has never visited a stock page"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EVER_PURCHASED_STOCK IS '{"comment":"This indicates whether the user has ever purchased a stock on US Stocks.","examples":[{"value":"1","explanation":"User has purchased a stock"},{"value":"0","explanation":"User has never purchased a stock"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_DISTINCT_STOCKS_BOUGHT_EVER IS '{"comment":"This represents the number of distinct stocks the user has ever bought.","examples":""}';
"""
)


vn.train(
    question="""how many stocks has actor 'A' bought ever? what are those stocks?""",
    sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. From this table we need the number of distinct stocks purchased and list of distinct stocks bought


select num_distinct_stocks_bought_ever, distinct_stocks_bought_ever 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where 1=1
    and actor_id = 'A'""",
)
vn.train(
    question="""I want to see monthwise total add fund transactions and amount for different add fund cohorts. First add fund month will be the cohort of the actor. For example my first add fund transaction was on 3rd jan 2024 I will be in Jan 2024 Cohort""",
    sql="""-- We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY A which has daily activity data of a user.This data is at an actor day level from this table we are extracting activity month, activity date and  number of wallet add fund transactions
-- Its joined with EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT. This is a user level table.  to get first add fund month
-- we have applied filters to select the actors for whom who added fund post jan 1st
B.first_success_add_fund_date >= '2024-01-01'
-- we use date_trunc(month, B.first_success_add_fund_date)  to extract month from date 
select  date_trunc(month, B.first_success_add_fund_date) as first_add_fund_month, 
        date_trunc(month, A.created_date_ist) as txn_month,
        sum(coalesce(A. num_wallet_add_fund_success_txns,0) ) as num_add_fund_txns,
        sum(coalesce(A. total_wallet_funds_added_usd,0)) as Total_Funds_added 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY A
left join 
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT B
on A. actor_id = B. actor_id
and A. created_date_ist >= B. first_success_add_fund_date
where B.first_success_add_fund_date >= '2024-01-01'
group by 1,2;""",
)
vn.train(
    question="""I need all need all the actor_ids and their moengage id of USS broker account holders """,
    sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table.  From this table we need account status of an actor and account status
-- We are joining USS_USER_BASE_FACT and EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B to get Moengage IDs. firehose_id in this table is actor_id in all USS tables. This table has one row per firehose_id (actor_id) 

-- we have applied account_status = 'ACTIVE' filter to filter in only USS broker account holders
-- we have selected actor_Id and firehose id as requried in the code
select actor_id, moengage_id
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT O
left join   EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS VM
   on O.actor_id= VM. firehose_id
where account_status = 'ACTIVE';""",
)
vn.train(
    question="""I want data of all users who have churned from US stock . I want to see all the stocks they purchased

We consider a user as churned if they have added greater than 15$ in their first add fund and their current AUM in less than 5$""",
    sql="""-- we are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. We need USS_USER_BASE_FACT to get the first success add fund amount and AUM USD, account status
-- In this sub query     (select actor_id, LISTAGG(DISTINCT A.stock_symbol, ', ') WITHIN GROUP (ORDER BY A.stock_symbol) as stocks_bought
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS A 
    where 1=1
        and txn_status = 'ORDER_SUCCESS'
        and type = 'BUY'
    group by 1) T we are creating a list of distinct stocks the user has bought
-- account_status = 'ACTIVE' is applied to filter in active uss account holders -- first_success_add_fund_amt_usd >= 15 and AUM_USD < 5 is the filter for churn
-- LISTAGG(DISTINCT A.stock_symbol, ', ') WITHIN GROUP (ORDER BY A.stock_symbol) this function is used to convert different entries in a row into a list
select O.actor_id, moengage_id, stocks_bought
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT O
left join   EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS VM
   on O.actor_id= VM. firehose_id
left join 
    (select actor_id, LISTAGG(DISTINCT A.stock_symbol, ', ') WITHIN GROUP (ORDER BY A.stock_symbol) as stocks_bought
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS A 
    where 1=1
        and txn_status = 'ORDER_SUCCESS'
        and type = 'BUY'
    group by 1) T
on O. actor_id = T. actor_id 
where 1=1
    and account_status = 'ACTIVE'
    and first_success_add_fund_amt_usd >= 15
    and AUM_USD < 5;""",
)
vn.train(
    question="""I want the count of different users in different add fund cohorts. First add fund month will be the cohort of the actor. For example my first add fund transaction was on 3rd jan 2024 I will be in Jan 2024 Cohort""",
    sql="""-- we are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. 

-- date_trunc(month, B.first_success_add_fund_date) is a function used to extract month from date
select date_trunc(month, B.first_success_add_fund_date) as first_add_fund_month, count(distinct B.actor_id) as total_actors
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT B
where 1=1
    and B.first_success_add_fund_date >= '2024-01-01'
group by 1;""",
)
vn.train(
    question="""I want actor ids and moengage ids of all actors who are invested in Nvidia""",
    sql="""-- this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here
-- We are joining USS_TRANSACTIONS and EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B to get Moengage IDs. firehose_id in this table is actor_id in all USS tables. This table has one row per firehose_id (actor_id) 
-- stock_symbol = 'NVDA' is applied to get transactions for NVDA
-- coalesce(bought_QTY ,0)- coalesce(sold_QTY,0) as active_qty gives us the current active quantity of us stocks
select  actor_id, MOENGAGE_ID
from 
(select actor_id,MOENGAGE_ID,
    sum(case when  type = 'BUY' then qty_confirmed end) as bought_QTY,
    sum(case when type = 'SELL' then qty_confirmed end) as sold_QTY,
    coalesce(bought_QTY ,0)- coalesce(sold_QTY,0) as active_qty
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS O
left join 
EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS VM
on O.actor_id= VM. firehose_id
where 1=1 
-- and side = 'BUY'
    and txn_status = 'ORDER_SUCCESS'
    and stock_symbol = 'NVDA'
group by 1,2)
where active_qty > 0;""",
)
vn.train(
    question="""Give me the stock ids of the following stocks 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'?
tell me about these stock symbols 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'.
are these stock ids active? 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'.""",
    sql="""-- We have used used EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS. This table contains all the stock level details. one row per stock. Contains details of Stocks and ETFs both

-- Its good to display internal_status, stock_type in such queries. these are good to know details of each stock
select Symbol, ID as stock_id  , internal_status, stock_type    
from EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS where symbol in ('BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM')
;""",
)
vn.train(
    question="""I want to see all the Wallet transactions in the last 7 weeks. Want to see User ID, Transaction_ID, time_stamp, order_type, status, amount , vendor account id. also need some user information like lifetime total add funds, Account creation date, first add fund date, last add fund date""",
    sql="""-- we have used 
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS. this table contains all wallet orders (or transactions). This table is joined with  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. We need USS_USER_BASE_FACT to get the user level information like account creation, total Add funds in the life time.
--  we have only considered ACTIVE Account holders using 
--  we have only considered wallet transactions of last 7 days using the created_date_ist column

select W.ACTOR_ID, W. wallet_transaction_id, W. created_at_ist,W. WALLET_ORDER_TYPE, W. status, W. amount_usd, A.vendor_account_id , A. total_wallet_funds_added_usd as LTD_Add_FUNDS, 
    A. acct_creation_date_ist as USS_Account_creation_date,
    date(A. first_success_add_fund_time) as first_add_fund_date,
    date(A. last_success_add_fund_date) as last_add_fund_date
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS W
left join 
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A
on W. actor_id = A. actor_id
where A. account_status = 'ACTIVE'
    and W. created_date_ist >= current_date() - 6 ;""",
)
vn.train(
    question="""I want to see all the Stock orders in last 7 days, Need the below information Actor_id, Transaction ID, order type, Status , Transaction Date , transaction amount , quantity, Stock symbol""",
    sql="""-- we have used  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here


select Actor_id, Txn_ID, Type, Txn_Status, TXN_CREATED_DATE, TXN_AMOUNT_CONFIRMED_USD, QTY_CONFIRMED, STOCK_SYMBOL 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where txn_created_date >= current_date() - 6;""",
)
vn.train(
    question="""I want D0, D7, D14, D30 and D365 Activation Rate/ Add Fund rate . Activation means first wallet add funds ever""",
    sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. From this table we need the account creation date and first successful add fund date
--  we have only considered ACTIVE Account holders using 
--  we have only considered account creations of last 90 days using the created_date_ist column
-- we have calculated D7_Activation_rate using  the below formula count(distinct case when  datediff(day, acct_creation_date_ist , first_success_add_fund_date) <= 6 then A.actor_id end )/ count(distinct A.actor_id) . Here we have counted the number of actors who successfully added funds in first 7 days of account creation
select 
        DATE(acct_creation_date_ist) as account_creation_date,
        date_TRUNC(WEEK, DATE(acct_creation_date_ist)) as account_creation_week,
        date_TRUNC(month, DATE(acct_creation_date_ist)) as account_creation_mth,
        count(distinct A. actor_id) as acct_creations,
        count(distinct case when  datediff(day, acct_creation_date_ist , first_success_add_fund_date) <= 0 then A.actor_id end )/ count(distinct A.actor_id) as   D0_Activation_Rate,
                count(distinct case when  datediff(day, acct_creation_date_ist , first_success_add_fund_date) <= 6 then A.actor_id end )/ count(distinct A.actor_id) as   D7_Activation_Rate,
            count(distinct case when  datediff(day, acct_creation_date_ist , first_success_add_fund_date) <= 13 then A.actor_id end )/ count(distinct A.actor_id) as   D14_Activation_Rate,
            count(distinct case when  datediff(day, acct_creation_date_ist , first_success_add_fund_date) <= 29 then A.actor_id end )/ count(distinct A.actor_id) as   D30_Activation_Rate,  
            count(distinct case when  datediff(day, acct_creation_date_ist , first_success_add_fund_date) <= 364 then A.actor_id end )/ count(distinct A.actor_id) as   D364_Activation_Rate 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A
where 1=1
    and account_status = 'ACTIVE'
    and date(acct_creation_start_time_ist) >= current_date()-90

group by 1,2,3 
order by 1;""",
)
vn.train(
    question="""Give details of about wallet transaction of a customer. need     ACTOR_ID,Transaction id,time to complete transaction in minutes,
    transaction timestamp,
    amount of transaction, transaction type""",
    sql="""-- We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS. this table contains all wallet orders (or transactions)


SELECT 
    ACTOR_ID,
    WALLET_TRANSACTION_ID,
    WALLET_TXN_TIME_TAKEN_MINS,
    CREATED_AT_IST,
    AMOUNT_USD
    ROW_NUMBER() OVER (PARTITION BY ACTOR_ID ORDER BY CREATED_AT_IST ASC) AS rn
FROM EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS
qualify rn =1;""",
)
vn.train(
    question="""I need all need all the actor_ids and their moengage id of USS broker account holders who have not added funds yet""",
    sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table.  From this table we need account status of an actor and first success_add_funds of an actor
-- We are joining USS_USER_BASE_FACT and EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B to get Moengage IDs. firehose_id in this table is actor_id in all USS tables. This table has one row per firehose_id (actor_id) 

-- we have applied account_status = 'ACTIVE' filter to filter in only USS broker account holders
-- we have applied  first_success_add_fund_date is null filter to filter in users who have not added any funds

select A.actor_id, B. moengage_id
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A    
left join 
EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B
on A. actor_id = B. firehose_id
where 1=1
    and account_status = 'ACTIVE'
    and first_success_add_fund_date is null""",
)
vn.train(
    question="""How many users bought the following stocks in the last 7 days and how amny transactions occured?
('NEM','IAU','GOLD','AAAU','FNV','GFI','AEM','GDX','AU')   """,
    sql="""-- we have used  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here
-- we have applied filter on stock_symbol column to filter in listed stocks
-- date filter is also applied to filter out last 7 days

select txn_created_date , count(*) as txns
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS A
where type = 'BUY'
    and stock_symbol in ('NEM','IAU','GOLD','AAAU','FNV','GFI','AEM','GDX','AU')   
    and txn_created_date >= current_date() - 6
group by 1
order by 1;""",
)
vn.train(
    question="""I want to see the monthly total add funds, total withdraw funds and the difference between them from January 1st 2024 onwards.""",
    sql="""-- EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY which has daily activity data of a user. This data is at an actor day level. From this table we are extracting activity month, activity date, and number of wallet add fund amount and wallet withdraw amount
we have applied filters to select the actors whose activity is from January 1st 2024 and onwards
we use date_trunc(month, created_date_ist) to extract month from date we have used sum(total_wallet_funds_added_usd) to extract the total funds added in a month, sum(total_wallet_funds_withdraw_usd) to extract total funds withdrawn in a month.
select date_trunc(month, created_date_ist) as mth, sum(total_wallet_funds_added_usd) as Add_funds, sum(total_wallet_funds_withdraw_usd) as WithdRAW_FUNDS, coalesce(Add_funds,0) - coalesce(WithdRAW_FUNDS,0) as total_wallet_funds_withdraw_usd from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY where 1=1 and created_date_ist >= '2024-01-01' group by 1;""",
)
