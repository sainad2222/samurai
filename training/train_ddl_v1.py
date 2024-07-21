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
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TABLE_REFRESH_TIME It is the time at which the table is refreshed. This is not a very important field and can be ignored for most queries."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ACTOR_ID It is the identifier for a user across the organization. This is a data point present across most tables in the organization where there is user action. Should be used as a joining key, since it represents the user identifier. examples { "35479187-1a5a-4dd2-80fd-695c2eb3f657", "20188659-94f0-46b2-bfb8-a3bdb3605f0d", "7b62cbda-a73f-4768-aa42-deced1ceaf5e"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_ID It is the identifier for a US Stocks Buy or Sell transaction. This is the primary key of this table and will remain unique. This is typically used for most of our developer debugging use-cases. examples { "USSOusxpKagKfr240618", "USSO48S8CJYuLE240618", "USSO2ii2jnEdL7240718"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.CLIENT_ORDER_ID Client order ID is the order ID which is sometimes used for debugging anything on Android or iOS clients. It is also a primary key and will remain unique. examples { "1b8a9688-2b62-4718-9b2a-ffd786562669", "715ce3d2-7bb0-4a72-babc-76342751bb32"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.VENDOR_ORDER_ID Vendor order ID is the order ID which is used for debugging orders with the downstream vendor. It is also a primary key and will remain unique."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.VENDOR_ACCOUNT_ID This is the unique identifier for a US Stocks brokerage account that is opened with the vendor. Typically used for debugging with the vendor."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.POOL_TXN_ORDER_ID This column can be ignored for this table."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WF_REQ_ID This is a column often used for debugging by the engineering team and checking the status of the workflows running behind the order. This is also a primary key for this table."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TYPE Type describes whether the order is a Buy order or Sell order. examples {"BUY": For when there is a buy order., "SELL": For when there is a sell order.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_STATUS Status describes the status of the order. examples {"ORDER_CANCELED": When a buy or sell order is placed & then canceled by the user., "ORDER_SUCCESS": For when an order is fulfilled by the vendor broker successfully., "ORDER_INITIATION_FAILED": For when order initiation with the vendor itself fails. This typically happens if there is a bug or a technical issue because orders don\'t get placed with the vendor., "ORDER_FAILED": For when the order gets placed, but the order fails.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_TIME_IST Time in IST when the order was placed by the user. examples {"2024-06-18T20:58:38.156Z"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_UPDATED_TIME_IST Time in IST when the order was most recently updated. examples {"2024-06-18T21:15:26.473Z"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_DATE Date in IST when the order was placed by the user. This is used to aggregate over a day. This is the most commonly used column for aggregating orders over a day. examples {"2024-06-18"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_UPDATED_DATE Date in IST when the order was most recently updated. This is used to aggregate over a day. examples {"2024-06-18"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_WEEK Date week in IST when the order was placed by the user. This is used to aggregate over a week. This is the most commonly used column for aggregating orders over a week. examples {"2024-06-18"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_CREATED_MONTH Date month in IST when the order was placed by the user. This is used to aggregate over a month. This is the most commonly used column for aggregating orders over a month. examples {"2024-06-01"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_AMOUNT_REQUESTED_USD This is the transaction amount in USD currency for which the order was placed. This is typically the column that should be referred to when checking for the order amount. examples {"1.000000"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.TXN_AMOUNT_CONFIRMED_USD This is the transaction amount in USD currency for which the order was confirmed and fulfilled. This is usually the same as TXN_AMOUNT_REQUESTED. examples {"1.000000"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.QTY_REQUESTED This is the quantity of the stock for which the order is requested. examples {"0.00649645943"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.QTY_CONFIRMED This is the quantity of the stock for which the order is confirmed. The value of it will be 0 for when the order status is not successful. examples {"0.012829128"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_PRICE_AT_REQUESTED_USD This is the price of the stock in USD when the US Stock order was placed. examples {"32.64"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_PRICE_AT_CONFIRMED_USD This is the price of the stock in USD when the US Stock order was confirmed. The value of it will be 0 for when the order status is not successful. examples {"32.64"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_SYMBOL Describes the ticker/symbol of the stock on the stock market. examples {"MSFT": MSFT is the symbol for Microsoft., "TSLA": TSLA is the symbol for Tesla., "NVDA": NVDA is the symbol for Nvidia.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_ID This is the unique identifier of a particular ticker/stock in the organization\'s tables. examples {"USS221228gbUTWdXyTEawkWJlQA+4qg=="}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_EXCHANGE This is the unique identifier of the exchange where the stock is listed on. examples {"EXCHANGE_NAS": For NASDAQ., "EXCHANGE_ASE": For American Stock Exchange., "EXCHANGE_ARCA": For Arca Stock Exchange, mostly ETFs listed here., "EXCHANGE_NYSE": For New York Stock Exchange., "EXCHANGE_BATS": For BATS Stock Exchange, mostly ETFs listed here.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_INTERNAL_STATUS Internal status defines whether the stock is active or disabled for buy. examples {"INTERNAL_STATUS_DISABLED_BUY": When the stock is disabled for buy., "INTERNAL_STATUS_AVAILABLE": When the stock is available for buy.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.MARKET_CATEGORY_NAME This defines the industry/market category to which the stock for which the order is placed belongs. examples {"Healthcare Plans", "Uranium", "Building Materials", "Broadcasting"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_COMPANY_NAME This defines the name of the company associated with the stock. examples {"Occidental Petroleum Corp", "GitLab Inc", "Autodesk Inc", "LivePerson Inc"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_INDUSTRY_ID This defines the industry ID of the stock. It is an attribute of a stock."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_INDUSTRY_GROUP_ID This defines the industry group ID of the stock. It is an attribute of a stock."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.STOCK_SECTOR_ID This defines the sector ID of the stock. It is an attribute of a stock."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_STAGE Each of the orders will be associated with a workflow which is running in the background. This defines the stage at which the workflow is at. The column is to be used when workflow-specific information is required. examples {"TRACK_ORDER": This is after the user\'s order is placed, whether it has been confirmed by the vendor broker., "SEND_SELL_ORDER": This is used for tracking whether the user\'s sell order is placed., "SEND_BUY_ORDER": This is used for tracking whether the user\'s buy order is placed.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_STATUS Each of the orders will be associated with a workflow which is running in the background. The workflow has various stages defined in the WORKFLOW_STAGE column. This defines the status of the stage of the workflow. examples {"MANUAL_INTERVENTION": When some error happens, a workflow goes into manual intervention for the engineer to fix manually., "SUCCESSFUL": Everything happened as expected., "CANCELED": Some user intervention happened to cancel the workflow., "FAILED": Some error occurred, which is a terminal error.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_VERSION This defines the version of the workflow. examples {"v0"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.WORKFLOW_TYPE This defines the workflow type, which can be a Buy transaction, Sell transaction, or a reward transaction. examples {"BUY_TRANSACTION": Represents a Buy transaction workflow., "SELL_TRANSACTION": Represents a Sell transaction workflow., "REWARD_TRANSACTION": Represents a reward transaction workflow. We should use this value when there are any stock reward-related queries.}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ACCOUNT_ID This defines the account ID that we have defined internally for a user's vendor broker account."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ACCOUNT_CREATED_TIME_IST This defines the time at which the user's vendor broker account is created in IST (Indian Standard Time)."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.DAYS_SINCE_ACCOUNT_CREATION This tells how many days it has been since the user has created the account."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.FIRST_INVEST_TIME_IST This tells the time in IST when a user invests in US Stocks for the first time during their lifetime. examples {"2024-06-18T20:58:38.156Z"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.NEW_REPEAT_USS This tells whether for that order, the user has invested for the first time in their lifetime or they are a repeat user. examples {"Repeat", "New"}'
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.SWIFT_TXN_ORDER_ID")
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.CATALOG_REF_ID")
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.EXTERNAL_ORDER_ID This tells the order ID which is visible to the end-user on their invoice. Hence the ID is used when there is a user issue on a specific order."
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.DELETED_AT_IST")
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.INVOICE_DETAILS")
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.PAYMENT_INFO")
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ORDER_COMPLETION_TIME_SEC This tells in seconds how much time it took for the order to get fulfilled from the order placement time."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ORDER_COMPLETION_TIME_MINS This tells in minutes how much time it took for the order to get fulfilled from the order placement time."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ORDER_COMPLETION_TIME_HOUR This tells in hours how much time it took for the order to get fulfilled from the order placement time."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.ORDER_COMPLETION_TIME_DAYS This tells in days how much time it took for the order to get fulfilled from the order placement time."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.PREV_CREATED_AT_IST This tells the timestamp of the previous successful order placed by the user if the user has placed an order before this."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS.DAYS_SINCE_PREV_INVESTED This tells the number of days since the previous successful order placed by the user if the user has placed an order before this."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TABLE_REFRESH_TIME It is the time at which the table is refreshed. This is not a very important field and can be ignored for most queries."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACTOR_ID It is the identifier for a user across the organization. This is a data point present across most tables in the organization where there is a user action. Should be used as a joining key, since it represents the user identifier. examples {"35479187-1a5a-4dd2-80fd-695c2eb3f657", "20188659-94f0-46b2-bfb8-a3bdb3605f0d", "7b62cbda-a73f-4768-aa42-deced1ceaf5e"}'
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCOUNT_ID")
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCOUNT_STATUS Describes the status of the US Stocks Account. Typically, this column is used only to check whether the account creation is done or not. Account creation is done when the status is "ACTIVE". In the rest of all cases, the account creation is not done regardless of the status. examples {"MANUAL_INTERVENTION": This means that the account creation is stuck because of some technical issue and is waiting for developer intervention to make it reach a terminal state., "INITIATED": When the account creation has started at the broker. It is not active yet., "KYC_VERIFIED": It means the account is not active yet., "CREATION_ON_HOLD": It means the account is not active yet., "ACTIVE": It means the account is active, "ACCOUNT_STATUS_UNSPECIFIED": It means the account is not active yet, "CREATED": It means the account is created but not active yet.}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.VENDOR_ACCOUNT_ID This is the unique identifier for a US Stocks brokerage account that is opened with the vendor. Typically used for debugging with the vendor. For any vendor use cases, the vendor account ID can be used."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EXTERNAL_ACCOUNT_ID This ID is different from both ACCOUNT_ID and VENDOR_ACCOUNT_ID. It is a user-friendly identifier intended for display to the user. It is not typically used for queries."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WF_REQ_ID WF stands for Workflow. For each account creation attempt, a unique workflow is created at the backend. This ID identifies that specific workflow and can be used for debugging purposes."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_ROW_DELETED_AT_IST"
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_STEP_CREATED_AT_IST This timestamp indicates when a user begins the US stocks suitability assessment, which is the first step in the US stocks account creation process."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_STEP_UPDATED_AT_IST This timestamp indicates when the US stocks suitability data is updated. Not frequently used."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DATE_OF_BIRTH This is the user's actual date of birth."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_RISK_LEVEL_OPTED This is the risk level the user opted for in the US Stocks suitability form. It indicates their willingness to take risks in investments. examples {"low-risk": User prefers investments with lower potential returns but also lower potential losses., "medium-risk": User is comfortable with a moderate level of risk for the potential of moderate returns., "high-risk": User is willing to accept higher risks for the possibility of higher returns.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_ITR_ENQUIRY This column indicates whether the user has filed an Income Tax Return (ITR) in the last 2 years, as part of the US Stocks suitability assessment. examples {"no-itr-filed-2-year": User has not filed an ITR in the last 2 years., "yes-itr-filed-2-year": User has filed an ITR in the last 2 years.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_EMPLOYMENT_TYPE This column indicates the user\'s employment type, as declared during the US Stocks suitability assessment. examples {"homemaker-employment": User identifies as a homemaker., "business-owner-professional-employment": User is a business owner or professional., "others-employment": User selected \'Other\' for employment type., "salaried-with-less-than-6-months-experience-employment": User is a salaried employee with less than 6 months of experience., "working-professional-employment": User is a working professional., "retired-employment": User is retired., "student-employment": User is a student., "self-employed-or-freelancer-employment": User is self-employed or a freelancer.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_INCOME_RANGE This column represents the user\'s self-reported income range, selected from predefined brackets, as part of the US Stocks suitability assessment. examples {"100000-500000", "2500000-10000000", "1000000-2500000", "500000-1000000", "10000000-25000000", "2500000-5000000", "5000000-10000000", "10000000-1000000000"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_INVESTED_INST This column stores a JSON array of the user\'s invested instruments, as declared in the US Stocks suitability assessment. The array represents the different types of investments the user currently holds. To query specific instruments within the array, JSON parsing will be required. examples { "["other-debtmf-sgbs-reits-investment"", ""overseas-investments-investment"", ""stock-equity-mutual-fund-investment"", ""physical-gold-real-state-investment""]", "["fixed-recurring-deposit-investment"", ""stock-equity-mutual-fund-investment"", ""overseas-investments-investment"", ""physical-gold-real-state-investment"", ""other-debtmf-sgbs-reits-investment""]", "["stock-equity-mutual-fund-investment"", ""other-debtmf-sgbs-reits-investment"", ""fixed-recurring-deposit-investment"", ""overseas-investments-investment"", ""physical-gold-real-state-investment""]"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_EDUCATION_QUALIFICATION This column indicates the user\'s highest level of education, as declared during the US Stocks suitability assessment. examples {"high-school-education-qualification": User has completed high school., "graduate-education-qualification": User has earned a bachelor\'s degree., "post-graduate-education-qualification": User has a master\'s degree or equivalent., "professional-degree-education-qualification": User holds a professional degree (e.g., MBA, JD, MD).}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_FORM_EXPECTED_AMOUNT_TO_INVEST This column describes the user\'s expected investment amount in US Stocks, using predefined text ranges. examples {"morethan-10k-lessthan-50k-expected-uss-investment", "morethan-1L-lessthan-5L-expected-uss-investment", "morethan-50k-lessthan-1L-expected-uss-investment", "lessthan-10K-expected-uss-investment", "morethan-5lakh-expected-uss-investment"}'
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DATE_OF_BIRTH_UNPARSED")
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_SCORE This score, ranging from 0-50, is generated based on the user's responses in the suitability assessment. A higher score indicates a greater suitability for investing in US Stocks. Factors influencing the score include income level, risk tolerance, and investment experience. For example, users with higher incomes, a greater willingness to take risks, and more investment experience are likely to have higher suitability scores."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.REMITTANCE_LIMIT_INR This is the maximum amount, in Indian Rupees (INR), that a user can invest in US Stocks within a financial year (April to March). This limit is a regulatory requirement set by our organization on international remittances allowed for US Stocks. In case this is 0 or null, the user is not allowed to make international remittances."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.SUITABILITY_STATUS This column indicates the user\'s current stage in the US Stocks suitability assessment process. examples {"SUITABILITY_STATUS_SCORE_CALCULATED": The user\'s suitability score has been calculated, and they are eligible to proceed., "SUITABILITY_STATUS_PROFILE_DATA_COLLECTED": The collection of suitability profile data is complete., "SUITABILITY_STATUS_USER_INELIGIBLE": The user is ineligible for international transactions., "SUITABILITY_STATUS_INITIATED": The suitability data collection process has been initiated.}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_IST This timestamp indicates when the user's US Stocks account was successfully created. It will be NULL if the account creation was not successful or has not yet occurred."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_DATE_IST This column represents the date on which the user's US Stocks account was successfully created. It is derived from ACCT_CREATION_TIME_IST and is useful for aggregations where the specific time of day is not required."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WEEK_IST This column represents the start date (Monday) of the week in which the user's US Stocks account was successfully created. It is used for weekly aggregations."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_MONTH_IST This column represents the first day of the month in which the user's US Stocks account was successfully created. It is used for monthly aggregations."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WORKFLOW_ID"
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WORKFLOW_STAGE This column indicates the specific stage of the account creation workflow where the user is currently at. It provides a more detailed breakdown of the progress compared to ACCOUNT_STATUS. examples {"US_BROKER_ACCOUNT_OPENING_COLLECT_AGREEMENTS": The account opening workflow is at the stage where it requests the user to agree to some agreements., "US_BROKER_ACCOUNT_OPENING_MANUAL_PAN_REVIEW": The account opening workflow is at a stage where the user goes into a manual PAN review which is done manually by the operations team at the back end., "US_BROKER_ACCOUNT_OPENING_COLLECT_SOURCE_OF_FUNDS": This represents the step when the user\'s source of funds document is being collected., "US_BROKER_ACCOUNT_OPENING_MANUAL_PAN_UPLOAD": This represents the step when the user is manually uploading their PAN in the account onboarding flow., "US_BROKER_ACCOUNT_OPENING_COLLECT_POA_AND_POI": This represents the step when the user is giving consent to collect their Proof of address & proof of identity, in case it is already available in our database., "USS_ACCOUNT_CREATION_ON_HOLD": This stage represents when even if the user completes all steps, their account could not be created because it doesn\'t meet one or another reason for not creating an account e.g. PAN uploaded was faulty, some required data is not available etc., "US_BROKER_ACCOUNT_OPENING_UPLOAD_KYC_DATA": This stage represents a backend step in the entire workflow and is typically an automated process to move ahead from this stage without user input., "US_BROKER_ACCOUNT_OPENING_COLLECT_RISK_DISCLOSURE": This stage represents a screen where we ask the users for a risk disclosure in case we feel a user may be risky., "US_BROKER_ACCOUNT_OPENING_COLLECT_EMPLOYMENT_DETAILS": This stage represents the employment details collection stage of the workflow., "US_BROKER_ACCOUNT_OPENING_ACCOUNT_OPENING_WITH_VENDOR": This stage represents when the account opening with the broker is being done. This should be an automated process., "US_BROKER_ACCOUNT_OPENING_AML_CHECK": This stage represents an Anti-money laundering check that is done at the back end before requesting an account opening., "US_BROKER_ACCOUNT_OPENING_WAIT_FOR_DOCUMENTS_UPLOAD": This stage is a backend step that waits for users\' documents to get uploaded., "US_BROKER_ACCOUNT_OPENING_POLL_ACCOUNT_STATUS": This stage is when the backend polls the vendor broker on what exactly the account opening status is., "US_BROKER_ACCOUNT_OPENING_FETCH_ADDRESS": This stage is a backend process when the user\'s address is being fetched from their account statement.}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WORKFLOW_STATUS"
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WORKFLOW_VERSION This column indicates the specific version of the account creation workflow that the user went through. Different versions of the workflow may have been used over time due to product updates or changes. examples {"V1": User went through version 1 of the workflow., "V0": User went through version 0 of the workflow.}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_WORKFLOW_TYPE"
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.CLIENT_REQ_ID")
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_START_TIME_IST This timestamp indicates precisely when the user initiated the US Stocks account creation process, marking their entry into the first stage of the workflow. examples {"2024-07-16T09:07:22.425Z"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_MINS This column records the total time taken, in minutes, to complete the US Stocks account creation process. It measures the duration from the user's first step in the workflow to the final stage. Importantly, this value will be NULL if the account is not yet active, indicating that the creation process is still ongoing."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_HOUR This column records the total time taken, in hours, to complete the US Stocks account creation process. It measures the duration from the user's first step in the workflow to the final stage. This value will be NULL if the account is not yet active."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCT_CREATION_TIME_DAYS This column records the total time taken, in days, to complete the US Stocks account creation process. It measures the duration from the user's first step in the workflow to the final stage. The value will be NULL if the account is not yet active."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_ACCOUNT_CREATED This column indicates the number of days that have elapsed since the user's US Stocks account was successfully created. It provides a measure of account age."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_WALLET_FUNDS_ADDED_USD This represents how much funds in USD the user has added to their US Broker wallet account since when they opened the account. examples {"1000.00", "5000.00", "200.00"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_WALLET_FUNDS_WITHDRAW_USD This represents how much money the user has withdrawn from their USD wallet over their lifetime."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_ADD_FUND_TXNS This is the number of successful add funds transactions that the user has done over their lifetime."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_WALLET_WITHDRAW_FUND_TXNS This is the number of successful withdrawal transactions the user has done since they created their account."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_WALLET_TXNS This represents how many successful wallet transactions the user has done in their lifetime. examples {"5"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_ADD_FUND_DATE This represents the date on which the user first added funds after account creation in their lifetime. This is an important column. examples {"2024-06-18"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_ADD_FUND_TIME This represents the time on which the user first added funds after account creation in their lifetime. This is an important column. examples {"2024-06-18T20:58:38.156Z"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_ADD_FUND_AMT_USD This represents the amount in USD of the first successful add funds transaction. This is an important column."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_WITHDRAW_FUND_DATE This represents the date on which the user first withdrew funds after account creation in their lifetime. This is an important column. examples {"2024-06-18"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_WITHDRAW_FUND_TIME This represents the time on which the user first withdrew funds after account creation in their lifetime. This is an important column. examples {"2024-06-18T20:58:38.156Z"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SUCCESS_WITHDRAW_FUND_AMT_USD This represents the amount in USD of the first successful withdraw funds transaction. This is an important column. examples {"13.50"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_ADD_FUND_DATE This represents the date on which the user has done their last successful add funds to the wallet transaction. examples {"2024-06-18"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_ADD_FUND_TIME This represents the time on which the user has done their last successful add funds to the wallet transaction. examples {"2024-06-18T20:58:38.156Z"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_ADD_FUND_AMT_USD This represents the amount in USD of the last successful add funds to the wallet transaction. examples {"12.60"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_WITHDRAW_FUND_DATE This represents the date on which the user has done their last successful withdraw funds from the wallet transaction. examples {"2024-06-18"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_WITHDRAW_FUND_TIME This represents the time on which the user has done their last successful withdraw funds from the wallet transaction. examples {"2024-06-18T20:58:38.156Z"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SUCCESS_WITHDRAW_FUND_AMT_USD This represents the amount in USD of the last successful withdraw funds from the wallet transaction."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.AUM_USD This represents the assets under management in USD that we have for the user. examples {"1208.40"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.AUM_USD_BUCKET This column has the bucket of amounts in USD. examples {">2K USD": More than 2000 USD, "1K-2K USD": Between 1000 USD and 2000 USD, "500-1K USD": Between 500 USD and 1000 USD, "<10 USD": Less than 10 USD, "10-100 USD": Between 10 USD and 100 USD, "100-500 USD": Between 100 USD and 500 USD}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCOUNT_CLOSED_TIME_IST"
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.ACCOUNT_CLOSED_DATE")
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_ORDERS This represents the number of stock buy or sell order attempts. This excludes any add funds or withdraw funds wallet orders and includes only buy or sell order attempts regardless of whether they are successful or failed."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_ORDERS This represents the number of successful stock buy or sell orders. This excludes any add funds or withdraw funds wallet orders and includes only buy or sell orders that got fulfilled successfully."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_BUY_ORDERS This represents the number of successful stock buy orders. This excludes any add funds or withdraw funds wallet orders and includes only buy orders that got fulfilled successfully."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_SUCCESS_SELL_ORDERS This represents the number of successful stock sell orders. This excludes any add funds or withdraw funds wallet orders and includes only sell orders that got fulfilled successfully."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_BUY_AMOUNT_USD This represents the total amount in USD of successful stock buy orders. It doesn't take into account orders that are still in progress or failed."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.TOTAL_SELL_AMOUNT_USD This represents the total amount in USD of successful stock sell orders. It doesn't take into account orders that are still in progress or failed."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_BOUGHT This represents the number of distinct stock symbols or stocks that the user has bought. If the user has bought Microsoft and Google stocks in the portfolio, then the number of distinct stocks is 2."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_SOLD This represents the number of distinct stock symbols or stocks that the user has sold."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_ORDER_DATE This represents the date on which the first buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_ORDER_WEEK This represents the week on which the first buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for week-based aggregations."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_ORDER_MONTH This represents the month on which the first buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for month-based aggregations."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_ORDER_DATE This represents the date on which the last buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_ORDER_WEEK This represents the week on which the last buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for week-based aggregations."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_ORDER_MONTH This represents the month on which the last buy or sell stock order was placed by the user. This does not include wallet add funds or withdraw orders. Use this column for month-based aggregations."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_AMOUNT_USD This represents the amount in USD for the first buy order that the user placed."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_QTY This represents the quantity of stocks that the user bought in their first-ever buy order on stocks."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_STOCK This is the symbol of the stock that the user bought first in their lifetime. examples {"MSFT": Microsoft, "INTC": Intel, "ADCT": ADC Telecommunications, "CVX": Chevron, "VNET": 22VNET Group, "CGAU": China Gas Holdings, "ONON": Onconova Therapeutics, "GLW": Corning, "BLDR": Builders FirstSource, "CRM": Salesforce}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_BUY_DATE This is the date on which the first buy order was placed by the user in their lifetime after account creation."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_AMOUNT_USD This represents the amount in USD for the first sell transaction that the user did ever after their vendor broker account creation."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_QTY This is the quantity of stock that the user sold in the first-ever sell transaction ever in their lifetime after account creation with the broker vendor."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_STOCK This is the symbol of the stock that the user sold first in their lifetime. examples {"MSFT": Microsoft, "INTC": Intel, "ADCT": ADC Telecommunications, "CVX": Chevron, "VNET": 22VNET Group, "CGAU": China Gas Holdings, "ONON": Onconova Therapeutics, "GLW": Corning, "BLDR": Builders FirstSource, "CRM": Salesforce}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.FIRST_SELL_DATE This is the date on which the user placed their first-ever sell transaction in their lifetime after account creation with the broker vendor."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_AMOUNT_USD This represents the amount in USD for the last buy order that the user placed."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_QTY This represents the quantity of stocks of the last buy order that the user placed."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_STOCK This is the symbol of the stock that the user bought last in their lifetime. examples {"MSFT": Microsoft, "INTC": Intel, "ADCT": ADC Telecommunications, "CVX": Chevron, "VNET": 22VNET Group, "CGAU": China Gas Holdings, "ONON": Onconova Therapeutics, "GLW": Corning, "BLDR": Builders FirstSource, "CRM": Salesforce}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_BUY_DATE The date on which the last buy order was placed by the user."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_AMOUNT_USD This is the amount in USD of the last sell order the user has placed."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_QTY This is the number of stocks that were sold by the user in their last sell order."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_STOCK This is the symbol of the stock that the user sold last in their lifetime. examples {"MSFT": Microsoft, "INTC": Intel, "ADCT": ADC Telecommunications, "CVX": Chevron, "VNET": 22VNET Group, "CGAU": China Gas Holdings, "ONON": Onconova Therapeutics, "GLW": Corning, "BLDR": Builders FirstSource, "CRM": Salesforce}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.LAST_SELL_DATE This is the date of the last sell transaction the user has ever placed."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_BOUGHT_EVER This represents the number of distinct stocks the user has ever bought."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_FIRST_ORDER This represents the number of days it has been since the user has placed their first buy or sell order."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_FIRST_BUY_ORDER This represents the number of days it has been since the user has placed their first buy order."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_FIRST_SELL_ORDER This represents the number of days it has been since the user has placed their first sell order."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_LAST_ORDER This represents the number of days it has been since the user has placed their last buy or sell order."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_LAST_BUY_ORDER This represents the number of days it has been since the user has placed their last buy order."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DAYS_SINCE_LAST_SELL_ORDER This represents the number of days it has been since the user has placed their last sell order."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_WATCHLISTED_CURRENT This represents the list of stocks that are watchlisted by the user at present. examples {"NVDA": User has NVDA in watchlist, "AAPL, AXP, CVX, KHC, KO, MCO, OXY": User has AAPL, AXP, CVX, KHC, KO, MCO, OXY in watchlist, "BBY": User has BBY in watchlist, "AAPL, AMZN, MSFT, NVDA, UBER, WMT": User has AAPL, AMZN, MSFT, NVDA, UBER, WMT in watchlist, "GFI": User has GFI in watchlist}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_DISTINCT_STOCKS_WATCHLISTED_CURRENT This represents the number of stocks that are watchlisted by the user at present."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.DISTINCT_STOCKS_VISITED This represents the list of stocks that are visited by the user ever. examples {"NVDA": User has visited NVDA, "AAPL, AXP, CVX, KHC, KO, MCO, OXY": User has visited AAPL, AXP, CVX, KHC, KO, MCO, OXY, "BBY": User has visited BBY, "AAPL, AMZN, MSFT, NVDA, UBER, WMT": User has visited AAPL, AMZN, MSFT, NVDA, UBER, WMT, "GFI": User has visited GFI}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_DISTINCT_STOCKS_VISITED This represents the number of distinct stocks that are visited by the user ever."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EVER_SEARCHED This indicates whether the user has ever used the search feature on US Stocks. It will be 1 if the user has searched, and will be null if the user has never searched."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.HAS_WATCHLISTED_CURRENT This indicates whether the user has currently watchlisted any stocks. examples {"1": User has watchlisted stocks, "null": User has not watchlisted any stocks}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EVER_VISITED_STOCK This indicates whether the user has ever visited a stock page on US Stocks. examples {"1": User has visited a stock page, "null": User has never visited a stock page}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.EVER_PURCHASED_STOCK This indicates whether the user has ever purchased a stock on US Stocks. examples {"1": User has purchased stock, "0": User has never purchased stock}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT.NUM_DISTINCT_STOCKS_BOUGHT_EVER This represents the number of distinct stocks the user has ever bought."
)
vn.train(ddl="EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.ID")
vn.train(
    ddl='EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.FIREHOSE_ID It is the identifier for a user across the organization. This is a data point present across most tables in the organization where there is a user action. Should be used as a joining key, since it represents the user identifier. examples {"35479187-1a5a-4dd2-80fd-695c2eb3f657", "20188659-94f0-46b2-bfb8-a3bdb3605f0d", "7b62cbda-a73f-4768-aa42-deced1ceaf5e"}'
)
vn.train(
    ddl='EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.MOENGAGE_ID It represents a user for the communication tool Moengage. Typically, this is used for sending any communications related to the user. examples {"0f8f515b-9cee-4f71-af1c-e213dcc33e15", "8204b606-213d-4749-84db-9f01e0487556", "cba1e02d-a65c-41d2-9005-088b50a57cfa", "805d5197-a7f3-43c8-b4bd-68d837f81cc3"}'
)
vn.train(ddl="EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.CREATED_AT")
vn.train(ddl="EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.UPDATED_AT")
vn.train(ddl="EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.CLIENT_APPSFLYER_ID")
vn.train(ddl="EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.PARTITION_COLUMN")
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.ID It is the internal stock ID which is the primary key of this table. This same column may be defined in other tables as Stock_ID. examples {"USS221228kEOfGr9/Q1+eDxOEDTfj3A==", "USS221228LuSNO1jVQSaUKFr5BNtv1A==", "USS221228CuQ1qt7aRCK8jrUOAQkqXw==", "USS230304ZAkbvww4QWujb8qxYKRy6g==", "USS2212289oVWPwfbQqSpfUhUH0SFGg==", "USS2212285F//JKotRJyI4fOVreOlLw==", "USS2212289k/WQIJWSHe6STo1P9Y0uw==", "USS22122872+TqjMmR4yYbyJn2stC5A=="}'
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.SYMBOL This is the stock symbol with which it trades on the exchange. This can also be used as a primary key and joining key across tables. examples {"NXGN": Symbol for NextGen Healthcare, "INDT": Symbol for Independent Bank Corp, "FRG": Symbol for First Republic Bank, "AMTB": Symbol for AMETEK Inc, "EVOP": Symbol for Evo Payments Inc, "NVTA": Symbol for Nvanta Inc, "NCR": Symbol for NCR Corp, "COUP": Symbol for Coupa Software Incorporated, "RE": Symbol for Realty Income Corp, "MNTV": Symbol for Monitord, "AAPL": Symbol for Apple}'
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.EXCHANGE Exchange represents the exchange where the symbol is listed and where the orders for it will be routed. examples {"EXCHANGE_NYSE": New York Stock Exchange, "EXCHANGE_NAS": NASDAQ Stock Exchange, "EXCHANGE_ASE": American Stock Exchange, "EXCHANGE_ARCA": NYSE Arca Stock Exchange, mostly ETFs are listed here, "EXCHANGE_BATS": Cboe BZX Exchange, mostly ETFs are listed here}'
)
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.DAILY_PERFORMANCE")
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.HISTORICAL_PRICE_DATA")
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.FI_CONTENT")
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.INTERNAL_STATUS It defines whether the stock is available to buy or not. examples {"INTERNAL_STATUS_UNAVAILABLE": The stock is unavailable to buy or sell, "INTERNAL_STATUS_AVAILABLE": The stock is available to buy or sell, "INTERNAL_STATUS_UNSPECIFIED": A rare instance where the availability is unknown, "INTERNAL_STATUS_DISABLED_BUY": Sell is allowed but buy is disabled}'
)
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.USER_AND_PLATFORM_SUPPORT")
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.CREATED_AT This represents when the stock was created in the system."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.UPDATED_AT This represents when the stock was last updated in the system."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.DELETED_AT This represents when the stock was deleted from the system."
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.STOCK_TYPE This defines the type of the stock. examples {"STOCK_TYPE_INDIVIDUAL_COMPANY": This represents an individual company stock, "STOCK_TYPE_ETF": This represents an Exchange Traded Fund (ETF)}'
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.INDUSTRY_ID This ID represents the industry to which the stock belongs and can be mapped to an industry name in another table. examples {"20645030", "10420030", "10280060"}'
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.INDUSTRY_GROUP_ID Similar to INDUSTRY_ID, this ID represents the industry group to which the stock belongs and can be mapped to an industry group name in another table."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.SECTOR_ID Similar to INDUSTRY_ID and INDUSTRY_GROUP_ID, this ID represents the sector to which the stock belongs and can be mapped to a sector name in another table."
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.COMPANY_INFO This column contains detailed information about the company associated with the stock in JSON format. The information includes company logo, market cap, website, name, type, address, contact details, description, employee info, and year of establishment. To access individual data points, the JSON object will need to be unmarshalled and parsed. examples {""{"logoUrl": "https://epifi-icons.s3.ap-south-1.amazonaws.com/usstocks_images/logos/128/NXGN.png", "marketCap": {"reportedDate": {"day": 13, "year": 2023, "month": 11}, "marketCapValue": {"units": "1606299642", "currencyCode": "USD"}, "enterpriseMarketCapValue": {"units": "1679500642", "currencyCode": "USD"}}, "websiteUrl": "https://www.nextgen.com"", "companyName"": {"shortName": "NextGen Healthcare"", "standardName": "NextGen Healthcare Inc""}, "companyType"": {}, "companyAddress"": {"city": "Atlanta"", "state": "GA"", "country"": "USA"", "addressLines"": ["3525 Piedmont Road""]}, "companyContactInfo"": {"personName"": "Rusty Frantz"", "professionalTitle"": "President & CEO""}, "companyDescription"": {"longDescription"": "NextGen Healthcare Inc is a United States-based company that provides healthcare solutions. The company offers technology and services platform supports for ambulatory and specialty practices of all sizes. It provides software, services, and analytics solutions to medical and dental group practices.""}, "companyEmployeeInfo"": {"totalEmployeeCount"": 2783, "fullTimeEmployeeCount"": 2783}, "yearOfEstablishment"": 1974}": Example JSON data for a company named NextGen Healthcare.}'
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.ESTIMATES_INFO This column stores analyst estimates and recommendations for the stock in JSON format. The data includes target price estimates (high, low, mean, median) and analyst recommendations (buy, sell, hold) with associated dates. To access specific data points, the JSON object needs to be unmarshalled and parsed. examples {""{"analystEstimates"": {"targetPriceEstimates"": {"periodicTargetPriceEstimates"": [{"low"": 23.95, "high"": 23.95, "mean"": 23.95, "median"": 23.95, "numOfEstimates"": 1}]}}, "analystRecommendations"": {"hold"": 1, "asOfDate"": {"day"": 10, "year"": 2023, "month"": 11}}}"": Example showing a hold recommendation and target price estimates for a stock.}'
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.FINANCIAL_INFO This column contains comprehensive financial information about the stock in JSON format. It includes yearly and quarterly data for: balance sheets, cash flow statements, income statements, growth ratios, valuation ratios, profitability ratios, and financial health ratios. Each data point is associated with a specific reporting date and period ending date. To access specific financial data, the JSON object needs to be unmarshalled and parsed. examples {""{"yearlyBalanceSheets"":[{"reportDate"":{"day"":31, "year"":2023, "month"":3}, "totalAssets"":{"units"":"896101000"", "currencyCode"":"USD""}, ...}]}": Shortened example showing a fragment of yearly balance sheet data.}'
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS.ID This is the primary key of the COLLECTIONS table, representing a unique identifier for a collection of US Stocks. Referred to as COLLECTION_ID in other parts of the database, it can be used as a joining key."
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS.DISPLAY_DETAILS This column contains a JSON object with all the display details of a collection. It includes elements like title, icon URL, subtitle, description, and discovery options. To access individual display details, the JSON object will need to be unmarshalled and parsed. examples {""{"title": "Tourism Titans", "iconUrl": "https://epifi-icons.s3.ap-south-1.amazonaws.com/flight.png", "subtitle": "Leading travel and tourism stocks", "description": "Industry giants that dominate the travel sector, from airlines and hotels to online travel agencies", "discoveryOptions": {"mainCollections": {"weight": 1, "visibility": "COLLECTION_VISIBILITY_VISIBLE"}}}"": Example JSON data for a collection called "Tourism Titans".}'
)
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS.CREATED_AT")
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS.UPDATED_AT")
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS.DELETED_AT")
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.COLLECTION_ID This represents the unique identifier of a collection and is a joining key that maps to the ID field in the COLLECTIONS table."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.STOCK_ID This is the internal identifier of a US Stock in the organization. It maps to the ID column in the STOCKS table and can be used for joining."
)
vn.train(ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.WEIGHT")
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.CREATED_AT"
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.UPDATED_AT"
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.DELETED_AT_UNIX"
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.ID This is the unique identifier for a watchlist, serving as the primary key of the table. It can be used as a joining key."
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.NAME This represents the name given to the watchlist by the user. examples {"My Tech Stocks": A watchlist named "My Tech Stocks", "Growth Potential": A watchlist named "Growth Potential"}'
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.CREATED_AT This indicates the timestamp when the watchlist was created."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.UPDATED_AT This indicates the timestamp when the watchlist was last updated."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.DELETED_AT This indicates the timestamp when the watchlist was deleted (if applicable)."
)
vn.train(
    ddl='EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.ACTOR_ID This is the identifier for the user who created the watchlist. This is a data point present across most tables in the organization where there is user action. Should be used as a joining key since it represents the user identifier. examples {"35479187-1a5a-4dd2-80fd-695c2eb3f657", "20188659-94f0-46b2-bfb8-a3bdb3605f0d", "7b62cbda-a73f-4768-aa42-deced1ceaf5e"}'
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.WATCHLIST_ID This represents the unique identifier of a watchlist and serves as a joining key that maps to the ID field in the WATCHLISTS table."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.STOCK_ID This is the internal identifier of a US Stock in the organization. It maps to the ID column in the STOCKS table and can be used for joining."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.CREATED_AT This indicates the timestamp when the stock was added to the watchlist."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.UPDATED_AT This indicates the timestamp when the mapping between the stock and watchlist was last updated."
)
vn.train(
    ddl="EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.DELETED_AT_UNIX This indicates the Unix timestamp when the stock was removed from the watchlist (if applicable)."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TABLE_REFRESH_TIME This represents the timestamp when the table was last refreshed."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.ACTOR_ID This is the identifier for a user across the organization. It can be used as a joining key to connect with user data in other tables. examples {"35479187-1a5a-4dd2-80fd-695c2eb3f657", "20188659-94f0-46b2-bfb8-a3bdb3605f0d", "7b62cbda-a73f-4768-aa42-deced1ceaf5e"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.CREATED_DATE_IST This represents the date in IST (Indian Standard Time) for which the user\'s daily activity is being recorded. Use this column for aggregating at a daily level. Use this date for any and all analysis on this table examples {"2024-06-18", "2024-06-19"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.LOADED_LANDING_PAGE This is a flag indicating whether the user loaded the US Stocks landing page on this particular date. examples {"1": The user loaded the landing page, "0": The user did not load the landing page}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.LOADED_WATCHLIST_PAGE This is a flag indicating whether the user loaded the watchlist page on this particular date. examples {"1": The user loaded the watchlist page, "0": The user did not load the watchlist page}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FIRED_SEARCH This is a flag indicating whether the user performed a search within the US Stocks section on this particular date. examples {"1": The user performed a search, "0": The user did not perform a search}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.LOADED_COLLECTION_PAGE This is a flag indicating whether the user loaded a collection page on this particular date. examples {"1": The user loaded a collection page, "0": The user did not load a collection page}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.VISITED_STOCK_PAGE This is a flag indicating whether the user visited any individual US stock details page on this particular date. examples {"1": The user visited a stock details page, "0": The user did not visit any stock details page}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_LOADED_LANDING_PAGE This represents the number of times the user loaded the US Stocks landing page on this particular date. examples {"5", "2", "10"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_LOADED_WATCHLIST_PAGE This represents the number of times the user loaded the watchlist page on this particular date. examples {"3", "1", "7"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_FIRED_SEARCH This represents the number of times the user performed a search within the US Stocks section on this particular date. examples {"2", "0", "8"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_LOADED_COLLECTION_PAGE This represents the number of times the user loaded a collection page on this particular date. examples {"4", "1", "6"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_VISITED_STOCK_PAGE This represents the number of times the user visited any individual stock page on this particular date. examples {"6", "2", "12"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_VISITED This is a comma-separated list of the distinct stock symbols the user visited on this particular date. examples {"AAPL,MSFT,GOOG": User visited pages for Apple, Microsoft, and Google stocks, "TSLA,AMZN": User visited pages for Tesla and Amazon stocks}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_DISTINCT_STOCKS_VISITED This represents the number of distinct stock symbols the user visited on this particular date. examples {"3", "2", "5"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_TXNS This represents the total number of wallet transactions (both add funds and withdraw funds) initiated by the user on this particular date. examples {"2", "0", "4"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_ADD_FUND_TXNS This represents the number of add funds transactions initiated by the user on this particular date. examples {"1", "0", "3"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_WITHDRAW_FUND_TXNS This represents the number of withdraw funds transactions initiated by the user on this particular date. examples {"1", "0", "2"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_SUCCESS_TXNS This represents the number of successful wallet transactions (both add funds and withdraw funds) completed by the user on this particular date. We typically use successful txn for querying and data analysis examples {"2", "0", "3"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_ADD_FUND_SUCCESS_TXNS This represents the number of successful add funds transactions completed by the user on this particular date. We typically use successful txn for querying and data analysis examples {"1", "0", "2"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.ADD_FUND_SUCCESS_FLAG This is a flag indicating whether the user had at least one successful add funds transaction on this particular date. examples {"1": The user had at least one successful add funds transaction, "0": The user attempted a transaction but was not successful in adding funds}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_WITHDRAW_FUND_SUCCESS_TXNS This represents the number of successful withdraw funds transactions completed by the user on this particular date. We typically use successful txn for querying and data analysis. The value will be null if the user did not attempt any withdraw funds transactions. examples {"1", "2", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.WITHDRAW_FUND_SUCCESS_FLAG This is a flag indicating whether the user had at least one successful withdraw funds transaction on this particular date. examples {"1": The user had at least one successful withdraw funds transaction, "0": The user attempted a withdraw funds transaction but it was not successful, "null": The user did not attempt any withdraw funds transactions}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.ADD_FUND_FAILURE_FLAG This is a flag indicating whether the user had at least one failed add funds transaction on this particular date. examples {"1": The user had at least one failed add funds transaction, "0": The user did not have any failed add funds transactions, "null": The user did not attempt any add funds transactions}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_WALLET_FUNDS_ADDED_USD This represents the total amount of funds in USD successfully added to the user\'s US Stocks broker wallet on this particular date. examples {"100.00", "500.50", "1000.00"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_WALLET_FUNDS_WITHDRAW_USD This represents the total amount of funds in USD successfully withdrawn from the user\'s US Stocks wallet on this particular date. examples {"50.00", "200.25", "500.00"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.AUM_DELTA_USD This represents the change in the user\'s Assets Under Management (AUM) in USD on this particular date. It reflects the net change due to wallet transactions and stock trades. examples {"150.00", "-50.25", "200.75"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILED_ADD_FUND_AMOUNT_USD This represents the total amount in USD of failed add funds transactions initiated by the user on this particular date. examples {"25.00", "0.00", "100.00"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.SUCCESS_ADD_FUND_AMOUNT_USD This represents the total amount in USD of successful add funds transactions completed by the user on this particular date. examples {"75.00", "500.50", "900.00"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.CREATED_ADD_FUND_AMOUNT_USD This represents the total amount in USD of add funds transactions initiated by the user on this particular date, regardless of their success or failure status. examples {"100.00", "500.50", "1000.00"}'
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.OTHERS_ADD_FUND_AMOUNT_USD")
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILURE_REASON_ADD_FUND This column provides the reason for failure for add funds transactions, if applicable. It will be null if there are no failed add funds transactions for the user on this date. examples {"WALLET_ORDER_FAILURE_REASON_OUTWARD_SWIFT_TRANSFER_FAILED": SWIFT transfer failed due to technical reasons or irregularities in forex., "WALLET_ORDER_FAILURE_REASON_LRS_LIMIT_BREACHED": Overall RBI limit for international remittance of $250,000 has been reached., "WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_FOR_DAY": Daily international remittance limit of 10L has been reached., "WALLET_ORDER_FAILURE_REASON_PAN_CHECK_FAILED_WITH_BANKING_PARTNER": User\'s PAN is ineligible for international remittances according to the bank; KYC actions are required., "WALLET_ORDER_FAILURE_REASON_INSUFFICIENT_NO_OF_TRANSACTIONS": User\'s bank account is not active enough and is considered risky., "WALLET_ORDER_FAILURE_REASON_KYC_CHECK_FAILED_WITH_BANKING_PARTNER": KYC check failed against the banking partner., "WALLET_ORDER_FAILURE_REASON_FOREIGN_REMITTANCE_NOT_ALLOWED": International remittances are not allowed for the user as per bank rejection., "WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_IN_FINANCIAL_YEAR": Regulatory limit set through suitability analysis has been breached., "WALLET_ORDER_FAILURE_REASON_SOF_REMITTANCE_LIMIT_BREACHED": Regulatory limit decided by the user\'s Source of Funds document has been reached., "null": No failed add funds transactions}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILED_WITHDRAW_FUND_AMOUNT_USD This represents the total amount in USD of failed withdraw funds transactions initiated by the user on this particular date. In case there is no withdraw amount failure for the user, then the value will be null examples {"50.00", "10.00", "200.00"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.SUCCESS_WITHDRAW_FUND_AMOUNT_USD This represents the total amount in USD of successful withdraw funds transactions completed by the user on this particular date. In case there\'s no successful withdraw transaction on that day for that user, the value will be null examples {"20.00", "200.25", "300.00"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.CREATED_WITHDRAW_FUND_AMOUNT_USD This represents the total amount in USD of withdraw funds transactions initiated by the user on this particular date, regardless of their success or failure status. This will be null in case there was no withdrawal attempted by the user on that day examples {"50.00", "200.25", "500.00"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.OTHER_WITHDRAW_FUND_AMOUNT_USD"
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILURE_REASON_WITHDRAW_FUND This column provides the reason for failure for withdraw funds transactions, if applicable. Currently, only one failure reason is tracked: WALLET_ORDER_FAILURE_REASON_UNSPECIFIED. The value will be null if there are no failed withdraw funds transactions for the user on this date. examples {"WALLET_ORDER_FAILURE_REASON_UNSPECIFIED": Unspecified reason for withdraw funds transaction failure., "null": No failed withdraw funds transactions}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_ORDERS This represents the total number of US Stock buy or sell order attempts (both buy and sell) made by the user on this particular date, including canceled or failed orders. The value will be null if there are no order attempts made by the user on this date. examples {"5", "10", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_BUY_ORDERS This represents the total number of US Stock buy order attempts made by the user on this particular date, including canceled or failed orders. The value will be null if there are no buy order attempts made by the user on this date. examples {"3", "7", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SELL_ORDERS This represents the total number of US Stock sell order attempts made by the user on this particular date, including canceled or failed orders. The value will be null if there are no sell order attempts made by the user on this date. examples {"2", "3", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SUCCESS_ORDERS This represents the total number of successful US Stock orders (both buy and sell) placed by the user on this particular date. We typically use successful orders for querying and data analysis. The value will be null if there are no successful orders placed by the user on this date. examples {"4", "8", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SUCCESS_BUY_ORDERS This represents the total number of successful US Stock buy orders placed by the user on this particular date. We typically use successful orders for querying and data analysis. The value will be null if there are no successful buy orders placed by the user on this date. examples {"2", "5", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SUCCESS_SELL_ORDERS This represents the total number of successful US Stock sell orders placed by the user on this particular date. We typically use successful orders for querying and data analysis. The value will be null if there are no successful sell orders placed by the user on this date. examples {"2", "3", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_BUY_AMOUNT_USD This represents the total value in USD of successful US Stock buy orders placed by the user on this particular date. The value will be null if there are no successful US Stock buy orders placed by the user on this date. examples {"2000.00", "5000.00", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_SELL_AMOUNT_USD This represents the total value in USD of successful US Stock sell orders placed by the user on this particular date. The value will be null if there are no successful US Stock sell orders placed by the user on this date. examples {"1500.00", "2500.00", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_TRADED This is a comma-separated list of the distinct US stock symbols the user has placed a successful buy or sell order in on this particular date. The value will be null if there are no successful buy or sell orders for the user on this date. examples {"AAPL,MSFT,GOOG": User placed a successful buy or sell order for Apple, Microsoft, and Google stocks, "TSLA,AMZN": User placed a successful buy or sell order for Tesla and Amazon stocks, "null": User did not place any successful buy or sell order}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_BOUGHT This represents the number of distinct US stock symbols the user successfully bought on this particular date. The value will be null if there are no successful US stock buy orders for the user on this date. examples {"3", "2", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_SOLD This represents the number of distinct US stock symbols the user successfully sold on this particular date. The value will be null if there are no successful US stock sell orders for the user on this date. examples {"2", "1", "null"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.WITHDRAW_FUND_FAILURE_FLAG This is a flag indicating whether the user had at least one failed withdraw funds transaction on this particular date. examples {"1": The user had at least one failed withdraw funds transaction, "0": The user did not have any failed withdraw funds transactions, "null": The user did not attempt any withdraw funds transactions}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.TABLE_REFRESH_TIME This represents the timestamp when the table was last refreshed."
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TRANSACTION_ID This is the unique identifier for a wallet transaction, serving as the primary key for this table. It is used to track individual add funds or withdraw funds requests. examples {"USSWO4EzRQvpHyC240716", "USSWO3tczkdvSUb240718", "USSWO3AXf76p19y240712"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.ACTOR_ID This is the identifier for a user across the organization. It represents the user who initiated the wallet transaction and can be used as a joining key to connect with user data in other tables. examples {"738a1cc8-0efa-4432-aa36-c4dda7627268", "25468f79-ed7e-4488-a8d8-ccd307d2a2f3", "ebe7ce8b-2e88-49c2-bfe3-b56980bff58a"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.USS_ACCOUNT_ID This is the unique identifier for a user\'s US Stocks brokerage account that is opened with the vendor. It represents the account associated with the wallet transaction. examples {"USSACCpp3AQIkLSTutA0M6dEsT8A240702==", "USSACCcnkiV/oCQyGw00obg4UU6A240719==", "USSACCJrPSNrQkTVWWq40uXM+UgA240331=="}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.EXTERNAL_ACCOUNT_ID This is the account_id, but shown to external users in a relatively more readable format. It is a counterpart to the USS Account ID. It is not that important of a column. examples {"363ab2aa4507344bbcecec1dcdb2896b870b3cbc6ca7a7725d694b1e87c810a6", "1cfe2ca413e8fd7a0ef3eaede99e3b6c1bdb3b5e180dab0ae753431f507fa096"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_AT_IST This timestamp indicates when the wallet transaction was created in IST (Indian Standard Time). It captures the precise moment the transaction request was initiated. examples {"2024-07-19 09:46:09.960"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_DATE_IST This field represents the date in IST when the wallet transaction was created. This column is frequently used for aggregating wallet transactions on a daily basis. It is generally the most reliable column for conducting any form of analysis on wallet transactions. examples {"2024-07-19"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_WEEK_IST This date field signifies the start of the week in IST during which the wallet transaction was created. It allows for analysis of wallet transaction trends or patterns on a weekly basis. examples {"2024-07-15"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_MONTH_IST This date field indicates the beginning of the month in IST when the wallet transaction was created. It is useful for tracking monthly transaction volumes or other month-over-month analyses. examples {"2024-07-01"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_AT_IST This timestamp field records the most recent update to the wallet transaction in IST. It captures the time of any status changes, modifications, or other relevant events related to the transaction. examples {"2024-07-19 19:02:25.052"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_DATE_IST This field represents the date in IST when the wallet transaction was most recently updated. It is often used to track the recency of changes or actions on the transaction. examples {"2024-07-19"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_WEEK_IST This date field signifies the start of the week in IST during which the wallet transaction was last updated. examples {"2024-07-15"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_MONTH_IST This date field indicates the beginning of the month in IST when the wallet transaction was last updated. examples {"2024-07-01"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.DELETED_AT_IST This timestamp field indicates when the wallet transaction was soft deleted in IST, if applicable. A non-null value suggests the transaction was removed or canceled at some point. It will be null if the wallet order is not deleted. examples {"2024-07-19 19:02:25.052"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.STATUS This field indicates the current status of the wallet order. examples {"WALLET_ORDER_STATUS_CREATED": The wallet order has been created successfully but is not yet fully processed., "WALLET_ORDER_STATUS_FAILED": The wallet order failed due to some reason., "WALLET_ORDER_STATUS_SUCCESS": The wallet order has been successfully completed., "WALLET_ORDER_STATUS_MANUAL_INTERVENTION": The wallet order requires manual intervention and debugging by an engineer due to a technical issue., "WALLET_ORDER_STATUS_INITIATION_FAILED": The wallet order initiation failed.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_ORDER_TYPE This field specifies the type of wallet order initiated by the user. examples {"WALLET_ORDER_TYPE_ADD_FUNDS": User initiated an international transaction to add funds to their USD wallet from their Indian bank account., "WALLET_ORDER_TYPE_WITHDRAW_FUNDS": User initiated an international transaction to withdraw funds from their USD wallet back to their Indian bank account.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_ORDER_TYPE_DERIVED This is a cleaner, more readable version of the \'WALLET_ORDER_TYPE\' column. It provides a user-friendly representation of the wallet order type. examples {"Add Funds": Represents an add funds wallet transaction, "Withdraw Funds": Represents a withdraw funds wallet transaction}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_ORDER_SUB_TYPE This field provides a more granular classification of the wallet order type. examples {"WALLET_ORDER_SUB_TYPE_UNSPECIFIED": Used for older wallet orders; can generally be ignored., "WALLET_ORDER_SUB_TYPE_ADD_FUNDS_REWARDS": Represents a reward credit added to the user\'s wallet automatically by Epifi., "WALLET_ORDER_SUB_TYPE_NON_INSTANT_WALLET_WITHDRAWAL": Represents a standard withdrawal transaction from the user\'s wallet., "WALLET_ORDER_SUB_TYPE_ADD_FUNDS_NON_INSTANT_WALLET_FUNDING": Represents a standard add funds transaction to the user\'s wallet.}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.FIRST_ADD_FUND_TIME_IST This timestamp captures the time in IST when the user made their very first successful 'Add Funds' transaction to their US Stocks wallet. This is a user-level attribute, not specific to individual wallet orders. examples {\"2024-06-18T20:58:38.156Z\"}"
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.NEW_REPEAT_ADDFUND_USS This field categorizes the user\'s wallet transaction based on whether it is their first ever user-initiated wallet transaction (excluding any previous reward transactions credited by the organization). examples {"New": This is the user\'s first wallet transaction initiated by them (excluding reward transactions)., "Repeat": The user has made wallet transactions before (excluding reward transactions).}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.AMOUNT_INR This field represents the transaction amount in INR (Indian Rupees). It applies to both Add Funds and Withdraw Funds transactions. examples {"2120.75"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.AMOUNT_USD This field represents the transaction amount in USD (US Dollars). It applies to both Add Funds and Withdraw Funds transactions. examples {"25"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.EXCHANGE_RATE This field indicates the USD/INR exchange rate used for the wallet transaction. The exchange rate is determined and can be updated during order processing but is fixed upon successful order completion. It will be the Buy exchange rate for Add Funds transactions and the Sell exchange rate for Withdraw Funds transactions. examples {"84.830000"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.LATEST_WF_STAGE This field represents the most recent stage of the workflow associated with processing the wallet transaction. Workflows vary depending on the transaction type (Add Funds, Withdraw Funds, Reward). examples {"TRACK_ORDER": For Reward transactions: System is monitoring whether the reward amount has been credited., "SEND_BUY_ORDER": For Reward transactions: Subsequent buy order request sent after reward amount credit., "TRACK_WALLET_FUND_TRANSFER": For Add Funds transactions: System is tracking the international transfer and crediting to the user\'s wallet., "REFUND_PAYMENT": For Add Funds transactions: Initiating or completing a refund due to a failed foreign funds transfer., "POOL_ACCOUNT_TRANSFER": For Add Funds transactions: User\'s payment has been credited to the bank\'s pool account., "FOREIGN_FUND_TRANSFER": For Add Funds transactions: Bank-initiated international transfer is in progress., "TRACK_INWARDS_REMITTANCE_STATUS": For Withdraw Funds transactions: Tracking the inward remittance of the withdrawal.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WF_REQ_ID This is a unique identifier for the workflow responsible for orchestrating the wallet order at the backend. It is used for tracking and managing the different stages of the wallet transaction process. examples {"WFRnH947AL0SW20JA6eHApLWw240719==", "WFRXqazdYL+Tj6vdMHo7x8fzQ240719=="}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.SWIFT_TXN_ID This field contains the SWIFT (International transaction) ID associated with the wallet transaction. It is only present for Add Funds transactions and will be null for other types. Note that this ID is not unique, as multiple transactions might be mapped to a single SWIFT. examples {"5555FOTT33124"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.POOL_TXN_ID This field stores the unique identifier for the payment transaction associated with the transfer to the pool account. It is primarily relevant for Add Funds transactions. examples {"117a4dc90d8158030aee170c99be934d594eae067e885a4a091491bf2d9fc56a", "68b0e89486fa9f7b7441bc5f72af777226ba6fb87e008b6a6eee5c657d17c011"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.INVOICE_DETAILS This field stores invoice details that are presented to the user in JSON format. It includes information like GST, TCS, amounts in INR and USD, the applied forex rate, and more. This JSON structure needs to be unmarshalled to access specific fields. examples {""{"GST": {"units": "45"", "currencyCode": "INR""}, "TCS": {"currencyCode": "INR""}, "amountInInr"": {"nanos"": 500000000, "units": "12724"", "currencyCode"": "INR""}, "amountInUSD"": {"units": "150"", "currencyCode": "USD""}, "forexRateId"": "FXwIodSqeFQn2QFM8obeMwzg240718=="", "totalDebitAmount"": {"nanos"": 500000000, "units": "12769"", "currencyCode": "INR""}, "forexRateProvenance"": "FOREX_RATE_PROVENANCE_MANUAL_PURCHASE"", "partnerExchangeRate"": {"nanos"": 830000000, "units": "84"", "currencyCode": "INR""}}": Example JSON structure containing invoice details. Key fields include: GST (amount and currency), TCS (currency), amountInInr, amountInUSD, forexRateId, totalDebitAmount, forexRateProvenance, partnerExchangeRate}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.AMOUNT_REQUESTED_JSON This field stores the originally requested transaction amount and currency in JSON format. The JSON needs to be unmarshalled to extract the amount and currency information. examples {""{"units"": 150, "currency_code"": ""USD""}"": Example JSON showing the requested amount (150) and currency (USD).}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.FAILURE_REASON This field provides the reason for the failure of the wallet order, if applicable. It will be null for successful orders. examples {"WALLET_ORDER_FAILURE_REASON_KYC_CHECK_FAILED_WITH_BANKING_PARTNER": KYC check failed with the banking partner., "WALLET_ORDER_FAILURE_REASON_SOF_REMITTANCE_LIMIT_BREACHED": Source of Funds remittance limit has been exceeded., "WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_IN_FINANCIAL_YEAR": Maximum allowed limit for adding funds in the financial year has been reached., "WALLET_ORDER_FAILURE_REASON_LRS_LIMIT_BREACHED": Liberalised Remittance Scheme (LRS) limit has been exceeded., "WALLET_ORDER_FAILURE_REASON_FOREIGN_REMITTANCE_NOT_ALLOWED": Foreign remittance is not allowed for the user based on bank or regulatory restrictions., "WALLET_ORDER_FAILURE_REASON_PAN_CHECK_FAILED_WITH_BANKING_PARTNER": PAN card check failed with the banking partner., "WALLET_ORDER_FAILURE_REASON_INSUFFICIENT_NO_OF_TRANSACTIONS": The user\'s bank account has insufficient transaction history and is considered risky., "WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_FOR_DAY": Maximum allowed limit for adding funds in a day has been reached., "WALLET_ORDER_FAILURE_REASON_UNSPECIFIED": Unspecified reason for failure., "WALLET_ORDER_FAILURE_REASON_ERROR_TRANSFERRING_AMOUNT_TO_POOL_ACCOUNT": Error transferring the amount to the pool account., "WALLET_ORDER_FAILURE_REASON_OUTWARD_SWIFT_TRANSFER_FAILED": The outward SWIFT transfer failed., "WALLET_ORDER_FAILURE_REASON_UNSPECIFIED": Unspecified reason for withdraw funds transaction failure., null: No failure reason. Order was successful.}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CLIENT_ORDER_ID This is the order ID which is sometimes used for debugging anything on Android or iOS clients. examples {"325968ea-6007-47f6-bdf5-2f172f60b316"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.VENDOR_ORDER_ID This is the unique identifier assigned to the wallet order by the vendor or payment processor. It is used for reconciliation and tracking transactions on the vendor\'s side. examples {"ab7e62aa-90c9-47d0-8403-c0f06cf8a782"}'
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.VENDOR_ACCOUNT_ID This is a unique identifier for the user's account on the vendor broker's platform. It is used to track and manage the user's funds and transactions with the vendor. examples {\"d7d1ad8acc6892f36539aac0a9319f656aa079cd3963699e9fe16fc9051ee975\"}"
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.EXTERNAL_ORDER_ID This is an order ID that is exposed externally to users, often for reference on invoices or during support interactions. examples {"BS5XFMsDnf1p"}'
)
vn.train(
    ddl='EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.PAYMENT_INFO This field provides additional payment-related information in JSON format, which may vary depending on the payment method used. examples {""{"utrNumber": "S10836315""}"": Example JSON structure containing payment info. In this case, it includes the UTR (Unique Transaction Reference) number.}'
)
vn.train(ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.REMITTANCE_REQ_ID")
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_SEC This field measures the total time taken for the wallet transaction to complete, expressed in seconds. It represents the duration from order creation to successful completion (or failure)."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_MINS This field measures the total time taken for the wallet transaction to complete, expressed in minutes. It represents the duration from order creation to successful completion (or failure)."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_HOUR This field measures the total time taken for the wallet transaction to complete, expressed in hours. It represents the duration from order creation to successful completion (or failure)."
)
vn.train(
    ddl="EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_DAYS This field measures the total time taken for the wallet transaction to complete, expressed in days. It represents the duration from order creation to successful completion (or failure)."
)
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.CHANNEL")
vn.train(
    ddl='EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.EVENT This field represents the name of the event. examples {"USSPreLaunchScreenLoad", "USSClickSort", "USSDetailsPageExited"}'
)
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.INTEGRATIONS")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.META")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.ORIGINALTIMESTAMP")
vn.train(
    ddl='EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.PROPERTIES It has the properties for the events in JSON form. The JSON will need to be unmarshalled to check all the properties. Refer to the document related to check the exact event and property required. examples {""{entry_point:HOME_SMART_DEPOSIT_TAB,entry_point_v2:HOME_SMART_DEPOSIT_TAB,event_id:2d89d837-6224-42c1-bac4-8bb1e52e6af9,funnel_start:"",opted_in:true,screen_name:default,session_id:605b15d6-1628-415a-9fdc-ce25ad523bb3,timestamp:1684918651696}""}'
)
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.RECEIVEDAT")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.SENTAT")
vn.train(
    ddl='EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.TIMESTAMP This field represents the exact time at which the time was fired. examples {"2023-05-24 08:57:31.696"}'
)
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.TYPE")
vn.train(
    ddl='EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.ACTOR_ID It is the identifier for a user across the organization. This is a data point present across most tables in the organization where there is a user action. Should be used as a joining key, since it represents the user identifier. examples {"35479187-1a5a-4dd2-80fd-695c2eb3f657", "20188659-94f0-46b2-bfb8-a3bdb3605f0d", "7b62cbda-a73f-4768-aa42-deced1ceaf5e"}'
)
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.APP")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.MANUFACTURER")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.MODEL")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.NETWORK")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.OS")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.EVENT_ID")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.EVENT_SOURCE")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.SCREEN_NAME")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.SESSION_ID")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.TIMESTAMP_IST")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.FAILURE_REASON")
vn.train(ddl="EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.PARTITION_COLUMN")
