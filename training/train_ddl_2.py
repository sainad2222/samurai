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

vn.train(ddl="""
--EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS

create or replace TABLE EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS (
	ID VARCHAR(16777216),
	FIREHOSE_ID VARCHAR(16777216),
	MOENGAGE_ID VARCHAR(16777216),
	CREATED_AT TIMESTAMP_NTZ(9),
	UPDATED_AT TIMESTAMP_NTZ(9),
	CLIENT_APPSFLYER_ID VARCHAR(16777216) WITH MASKING POLICY #unknown_policy,
	PARTITION_COLUMN VARCHAR(16777216)
);

COMMENT ON TABLE EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS IS '{ "comment": "The only 2 important columns are moengage ID and firehose ID. This table is primarily used for mapping the firehose id which represents the actor ID or actors to the firehose ID"}'

COMMENT ON COLUMN EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.FIREHOSE_ID IS '{ "comment": "It is the identifier for a user across the organisation. This is a data point present across most tables in the organisation where there is a user action. Should be used as a joining key, since it represents the user identifier.","examples": ["35479187-1a5a-4dd2-80fd-695c2eb3f657","20188659-94f0-46b2-bfb8-a3bdb3605f0d","7b62cbda-a73f-4768-aa42-deced1ceaf5e"]}';

COMMENT ON COLUMN EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS.MOENGAGE_ID IS '{ "comment": "It represents a user for the communication tool Moengage. Typically, this is used for sending any communications related to the user.","examples": ["0f8f515b-9cee-4f71-af1c-e213dcc33e15","8204b606-213d-4749-84db-9f01e0487556","cba1e02d-a65c-41d2-9005-088b50a57cfa","805d5197-a7f3-43c8-b4bd-68d837f81cc3"]}';
""")

vn.train(ddl="""
create or replace TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS (
	ID VARCHAR(16777216),
	SYMBOL VARCHAR(16777216),
	EXCHANGE VARCHAR(16777216),
	DAILY_PERFORMANCE VARCHAR(16777216),
	HISTORICAL_PRICE_DATA VARCHAR(16777216),
	FI_CONTENT VARCHAR(16777216),
	INTERNAL_STATUS VARCHAR(16777216),
	USER_AND_PLATFORM_SUPPORT VARCHAR(16777216),
	CREATED_AT TIMESTAMP_NTZ(9),
	UPDATED_AT TIMESTAMP_NTZ(9),
	DELETED_AT TIMESTAMP_NTZ(9),
	STOCK_TYPE VARCHAR(16777216),
	INDUSTRY_ID VARCHAR(16777216),
	INDUSTRY_GROUP_ID VARCHAR(16777216),
	SECTOR_ID VARCHAR(16777216),
	COMPANY_INFO VARCHAR(16777216),
	ESTIMATES_INFO VARCHAR(16777216),
	FINANCIAL_INFO VARCHAR(16777216)
);

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.ID IS '{"comment":"It is the internal stock ID which is the primary key of this table. This same column may be defined in other tables as Stock_ID.","examples": ["USS221228kEOfGr9/Q1+eDxOEDTfj3A==","USS221228LuSNO1jVQSaUKFr5BNtv1A==","USS221228CuQ1qt7aRCK8jrUOAQkqXw==","USS230304ZAkbvww4QWujb8qxYKRy6g==","USS2212289oVWPwfbQqSpfUhUH0SFGg==","USS2212285F//JKotRJyI4fOVreOlLw==","USS2212289k/WQIJWSHe6STo1P9Y0uw==","USS22122872+TqjMmR4yYbyJn2stC5A=="]}';

COMMENT ON TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS IS 'The stocks table contains all the information about a stock in its table. This includes data about it’s stock ID to symbol mapping, the stock type, the industry ID it belongs, the sector ID, the industry group ID. It also contains subjective information about the company like address, what the company does, the logo as well as financial information like revenue, profits etc. as well as analyst estimates, like buy, sell recommendations target price estimates etc. Anything and everything about a stock is available in this table.';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.SYMBOL IS '{"comment":"This is the stock symbol with which it trades on the exchange. This can also be used as primary key and joining key across tables.","examples":[{"value":"NXGN","explanation":"Symbol for NextGen Healthcare"},{"value":"INDT","explanation":"Symbol for Independent Bank Corp"},{"value":"FRG","explanation":"Symbol for First Republic Bank"},{"value":"AMTB","explanation":"Symbol for AMETEK Inc"},{"value":"EVOP","explanation":"Symbol for Evo Payments Inc"},{"value":"NVTA","explanation":"Symbol for  Nvanta Inc"},{"value":"NCR","explanation":"Symbol for NCR Corp"},{"value":"COUP","explanation":"Symbol for Coupa Software Incorporated"},{"value":"RE","explanation":"Symbol for Realty Income Corp"},{"value":"MNTV","explanation":"Symbol for  Monitord"},{"value":"AAPL","explanation":"Symbol for Apple"}]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.EXCHANGE IS '{"comment":"Exchange represents the exchange where the symbol is listed and where the orders for it will be routed.","examples":[{"value":"EXCHANGE_NYSE","explanation":"New York Stock Exchange"},{"value":"EXCHANGE_NAS","explanation":"NASDAQ Stock Exchange"},{"value":"EXCHANGE_ASE","explanation":"American Stock Exchange"},{"value":"EXCHANGE_ARCA","explanation":"NYSE Arca Stock Exchange, mostly ETFs are listed here"},{"value":"EXCHANGE_BATS","explanation":"Cboe BZX Exchange, mostly ETFs are listed here"}]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.INTERNAL_STATUS IS '{"comment":"It defines whether the stock is available to buy or not.","examples":[{"value":"INTERNAL_STATUS_UNAVAILABLE","explanation":"The stock is unavailable to buy or sell"},{"value":"INTERNAL_STATUS_AVAILABLE","explanation":"The stock is available to buy or sell"},{"value":"INTERNAL_STATUS_UNSPECIFIED","explanation":"A rare instance where the availability is unknown"},{"value":"INTERNAL_STATUS_DISABLED_BUY","explanation":"Sell is allowed but buy is disabled"}]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.CREATED_AT IS '{"comment":"This represents when the stock was created in the system."}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.UPDATED_AT IS '{"comment":"This represents when the stock was last updated in the system."}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.DELETED_AT IS '{"comment":"This represents when the stock was deleted from the system."}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.STOCK_TYPE IS '{"comment":"This defines the type of the stock.","examples":[{"value":"STOCK_TYPE_INDIVIDUAL_COMPANY","explanation":"This represents an individual company stock"},{"value":"STOCK_TYPE_ETF","explanation":"This represents an Exchange Traded Fund (ETF)"}]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.INDUSTRY_ID IS '{"comment":"This ID represents the industry to which the stock belongs and can be mapped to an industry name in another table.","examples":["20645030","10420030","10280060"]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.INDUSTRY_GROUP_ID IS '{"comment":"Similar to INDUSTRY_ID, this ID represents the industry group to which the stock belongs and can be mapped to an industry group name in another table.","examples":"}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.SECTOR_ID IS '{"comment":"Similar to INDUSTRY_ID and INDUSTRY_GROUP_ID, this ID represents the sector to which the stock belongs and can be mapped to a sector name in another table.","examples":"}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.COMPANY_INFO IS '{"comment":"This column contains detailed information about the company associated with the stock in JSON format. The information includes company logo, market cap, website, name, type, address, contact details, description, employee info, and year of establishment.  To access individual data points, the JSON object will need to be unmarshalled and parsed.","examples":[{"value":"{\\"logoUrl\\": \\"https://epifi-icons.s3.ap-south-1.amazonaws.com/usstocks_images/logos/128/NXGN.png\\", \\"marketCap\\": {\\"reportedDate\\": {\\"day\\": 13, \\"year\\": 2023, \\"month\\": 11}, \\"marketCapValue\\": {\\"units\\": \\"1606299642\\", \\"currencyCode\\": \\"USD\\"}, \\"enterpriseMarketCapValue\\": {\\"units\\": \\"1679500642\\", \\"currencyCode\\": \\"USD\\"}}, \\"websiteUrl\\": \\"https://www.nextgen.com\\", \\"companyName\\": {\\"shortName\\": \\"NextGen Healthcare\\", \\"standardName\\": \\"NextGen Healthcare Inc\\"}, \\"companyType\\": {}, \\"companyAddress\\": {\\"city\\": \\"Atlanta\\", \\"state\\": \\"GA\\", \\"country\\": \\"USA\\", \\"addressLines\\": [\\"3525 Piedmont Road\\"]}, \\"companyContactInfo\\": {\\"personName\\": \\"Rusty Frantz\\", \\"professionalTitle\\": \\"President & CEO\\"}, \\"companyDescription\\": {\\"longDescription\\": \\"NextGen Healthcare Inc is a United States-based company that provides healthcare solutions. The company offers technology and services platform supports for ambulatory and specialty practices of all sizes. It provides software, services, and analytics solutions to medical and dental group practices.\\"}, \\"companyEmployeeInfo\\": {\\"totalEmployeeCount\\": 2783, \\"fullTimeEmployeeCount\\": 2783}, \\"yearOfEstablishment\\": 1974}","explanation":"Example JSON data for a company named NextGen Healthcare."}]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.ESTIMATES_INFO IS '{"comment":"This column stores analyst estimates and recommendations for the stock in JSON format.  The data includes target price estimates (high, low, mean, median) and analyst recommendations (buy, sell, hold) with associated dates. To access specific data points, the JSON object needs to be unmarshalled and parsed.","examples":[{"value":"{\\"analystEstimates\\": {\\"targetPriceEstimates\\": {\\"periodicTargetPriceEstimates\\": [{\\"low\\": 23.95, \\"high\\": 23.95, \\"mean\\": 23.95, \\"median\\": 23.95, \\"numOfEstimates\\": 1}]}}, \\"analystRecommendations\\": {\\"hold\\": 1, \\"asOfDate\\": {\\"day\\": 10, \\"year\\": 2023, \\"month\\": 11}}}","explanation":"Example showing a hold recommendation and target price estimates for a stock."}]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS.FINANCIAL_INFO IS '{"comment":"This column contains comprehensive financial information about the stock in JSON format. It includes yearly and quarterly data for: balance sheets, cash flow statements, income statements, growth ratios, valuation ratios, profitability ratios, and financial health ratios. Each data point is associated with a specific reporting date and period ending date. To access specific financial data, the JSON object needs to be unmarshalled and parsed.","examples":[{"value":"{\\"yearlyBalanceSheets\\":[{\\"reportDate\\":{\\"day\\":31, \\"year\\":2023, \\"month\\":3}, \\"totalAssets\\":{\\"units\\":\\"896101000\\", \\"currencyCode\\":\\"USD\\"}, ...}]}", "explanation":"Shortened example showing a fragment of yearly balance sheet data."}]}';
""")


vn.train(ddl="""
create or replace TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS (
	ID VARCHAR(16777216),
	DISPLAY_DETAILS VARCHAR(16777216),
	CREATED_AT TIMESTAMP_NTZ(9),
	UPDATED_AT TIMESTAMP_NTZ(9),
	DELETED_AT TIMESTAMP_NTZ(9)
);

COMMENT ON TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS IS 'A collection is a curated group of US Stocks. This table contains data about the display details of these collections and is primarily used for understanding how a collection should be presented.';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS.ID IS '{"comment":"This is the primary key of the COLLECTIONS table, representing a unique identifier for a collection of US Stocks. Referred to as COLLECTION_ID in other parts of the database, it can be used as a joining key.","examples":"}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTIONS.DISPLAY_DETAILS IS '{"comment":"This column contains a JSON object with all the display details of a collection. It includes elements like title, icon URL, subtitle, description, and discovery options. To access individual display details, the JSON object will need to be unmarshalled and parsed.","examples":[{"value":"{\\"title\\": \\"Tourism Titans\\", \\"iconUrl\\": \\"https://epifi-icons.s3.ap-south-1.amazonaws.com/flight.png\\", \\"subtitle\\": \\"Leading travel and tourism stocks\\", \\"description\\": \\"Industry giants that dominate the travel sector, from airlines and hotels to online travel agencies\\", \\"discoveryOptions\\": {\\"mainCollections\\": {\\"weight\\": 1, \\"visibility\\": \\"COLLECTION_VISIBILITY_VISIBLE\\"}}}","explanation":"Example JSON data for a collection called \\"Tourism Titans\\"."}]}';
""")

vn.train(ddl="""
"create or replace TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS (
	COLLECTION_ID VARCHAR(16777216),
	STOCK_ID VARCHAR(16777216),
	WEIGHT NUMBER(38,0),
	CREATED_AT TIMESTAMP_NTZ(9),
	UPDATED_AT TIMESTAMP_NTZ(9),
	DELETED_AT_UNIX NUMBER(38,0)
);

COMMENT ON TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS IS 'This table maps individual US Stocks to specific collections. It defines which collections have which stocks.';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.COLLECTION_ID IS '{"comment":"This represents the unique identifier of a collection and is a joining key that maps to the ID field in the COLLECTIONS table.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS.STOCK_ID IS '{"comment":"This is the internal identifier of a US Stock in the organization. It maps to the ID column in the STOCKS table and can be used for joining.","examples":""}';"
""")

vn.train(ddl="""
"create or replace TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS (
	ID VARCHAR(16777216),
	NAME VARCHAR(16777216),
	CREATED_AT TIMESTAMP_NTZ(9),
	UPDATED_AT TIMESTAMP_NTZ(9),
	DELETED_AT TIMESTAMP_NTZ(9),
	ACTOR_ID VARCHAR(16777216)
);

COMMENT ON TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS IS 'This table stores information about watchlists created by users to track specific US Stocks.';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.ID IS '{"comment":"This is the unique identifier for a watchlist, serving as the primary key of the table. It can be used as a joining key.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.NAME IS '{"comment":"This represents the name given to the watchlist by the user.","examples":[{"value":"My Tech Stocks","explanation":"A watchlist named \\"My Tech Stocks\\""},{"value":"Growth Potential","explanation":"A watchlist named \\"Growth Potential\\""}]}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.CREATED_AT IS '{"comment":"This indicates the timestamp when the watchlist was created.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.UPDATED_AT IS '{"comment":"This indicates the timestamp when the watchlist was last updated.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.DELETED_AT IS '{"comment":"This indicates the timestamp when the watchlist was deleted (if applicable).","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS.ACTOR_ID IS '{"comment":"This is the identifier for the user who created the watchlist. This is a data point present across most tables in the organization where there is a user action. Should be used as a joining key since it represents the user identifier.","examples":["35479187-1a5a-4dd2-80fd-695c2eb3f657","20188659-94f0-46b2-bfb8-a3bdb3605f0d","7b62cbda-a73f-4768-aa42-deced1ceaf5e"]}'; "
""")

vn.train(ddl="""
"create or replace TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS (
	WATCHLIST_ID VARCHAR(16777216),
	STOCK_ID VARCHAR(16777216),
	CREATED_AT TIMESTAMP_NTZ(9),
	UPDATED_AT TIMESTAMP_NTZ(9),
	DELETED_AT_UNIX NUMBER(38,0)
);

COMMENT ON TABLE EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS IS 'This table maps individual US Stocks to specific watchlists, indicating which stocks a user has added to their watchlist.';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.WATCHLIST_ID IS '{"comment":"This represents the unique identifier of a watchlist and serves as a joining key that maps to the ID field in the WATCHLISTS table.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.STOCK_ID IS '{"comment":"This is the internal identifier of a US Stock in the organization. It maps to the ID column in the STOCKS table and can be used for joining.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.CREATED_AT IS '{"comment":"This indicates the timestamp when the stock was added to the watchlist.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.UPDATED_AT IS '{"comment":"This indicates the timestamp when the mapping between the stock and watchlist was last updated.","examples":""}';

COMMENT ON COLUMN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS.DELETED_AT_UNIX IS '{"comment":"This indicates the Unix timestamp when the stock was removed from the watchlist (if applicable).","examples":""}';"
""")

vn.train(ddl=""" 
"create or replace TRANSIENT TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY (
	TABLE_REFRESH_TIME TIMESTAMP_LTZ(9),
	ACTOR_ID VARCHAR(16777216),
	CREATED_DATE_IST DATE,
	LOADED_LANDING_PAGE NUMBER(1,0),
	LOADED_WATCHLIST_PAGE NUMBER(1,0),
	FIRED_SEARCH NUMBER(1,0),
	LOADED_COLLECTION_PAGE NUMBER(1,0),
	VISITED_STOCK_PAGE NUMBER(1,0),
	NUM_LOADED_LANDING_PAGE NUMBER(18,0),
	NUM_LOADED_WATCHLIST_PAGE NUMBER(18,0),
	NUM_FIRED_SEARCH NUMBER(18,0),
	NUM_LOADED_COLLECTION_PAGE NUMBER(18,0),
	NUM_VISITED_STOCK_PAGE NUMBER(18,0),
	DISTINCT_STOCKS_VISITED VARCHAR(16777216),
	NUM_DISTINCT_STOCKS_VISITED NUMBER(18,0),
	NUM_WALLET_TXNS NUMBER(18,0),
	NUM_WALLET_ADD_FUND_TXNS NUMBER(18,0),
	NUM_WALLET_WITHDRAW_FUND_TXNS NUMBER(18,0),
	NUM_WALLET_SUCCESS_TXNS NUMBER(18,0),
	NUM_WALLET_ADD_FUND_SUCCESS_TXNS NUMBER(18,0),
	ADD_FUND_SUCCESS_FLAG NUMBER(1,0),
	NUM_WALLET_WITHDRAW_FUND_SUCCESS_TXNS NUMBER(18,0),
	WITHDRAW_FUND_SUCCESS_FLAG NUMBER(1,0),
	ADD_FUND_FAILURE_FLAG NUMBER(1,0),
	WITHDRAW_FUND_FAILURE_FLAG NUMBER(1,0),
	TOTAL_WALLET_FUNDS_ADDED_USD FLOAT,
	TOTAL_WALLET_FUNDS_WITHDRAW_USD FLOAT,
	AUM_DELTA_USD FLOAT,
	FAILED_ADD_FUND_AMOUNT_USD FLOAT,
	SUCCESS_ADD_FUND_AMOUNT_USD FLOAT,
	CREATED_ADD_FUND_AMOUNT_USD FLOAT,
	OTHERS_ADD_FUND_AMOUNT_USD FLOAT,
	FAILURE_REASON_ADD_FUND VARCHAR(16777216),
	FAILED_WITHDRAW_FUND_AMOUNT_USD FLOAT,
	SUCCESS_WITHDRAW_FUND_AMOUNT_USD FLOAT,
	CREATED_WITHDRAW_FUND_AMOUNT_USD FLOAT,
	OTHER_WITHDRAW_FUND_AMOUNT_USD FLOAT,
	FAILURE_REASON_WITHDRAW_FUND VARCHAR(16777216),
	NUM_ORDERS NUMBER(18,0),
	NUM_BUY_ORDERS NUMBER(18,0),
	NUM_SELL_ORDERS NUMBER(18,0),
	NUM_SUCCESS_ORDERS NUMBER(18,0),
	NUM_SUCCESS_BUY_ORDERS NUMBER(18,0),
	NUM_SUCCESS_SELL_ORDERS NUMBER(18,0),
	TOTAL_BUY_AMOUNT_USD NUMBER(38,6),
	TOTAL_SELL_AMOUNT_USD NUMBER(38,6),
	DISTINCT_STOCKS_TRADED VARCHAR(16777216),
	DISTINCT_STOCKS_BOUGHT NUMBER(18,0),
	DISTINCT_STOCKS_SOLD NUMBER(18,0)
);

COMMENT ON TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY IS 'This table provides a comprehensive view of user behavior on US Stocks at a User X Day level. It contains flags and metrics indicating user actions like page visits, searches, wallet transactions, and stock orders. Ideal for daily or period-over-period analysis by aggregating daily data, it acts as a daily user base fact table.';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TABLE_REFRESH_TIME IS '{"comment":"This represents the timestamp when the table was last refreshed.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.ACTOR_ID IS '{"comment":"This is the identifier for a user across the organization. It can be used as a joining key to connect with user data in other tables.","examples":["35479187-1a5a-4dd2-80fd-695c2eb3f657","20188659-94f0-46b2-bfb8-a3bdb3605f0d","7b62cbda-a73f-4768-aa42-deced1ceaf5e"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.CREATED_DATE_IST IS '{"comment":"This represents the date in IST (Indian Standard Time) for which the users daily activity is being recorded.","examples":["2024-06-18","2024-06-19"]}. Use this column for aggregating at a daily level. Use this date for any and all analysis on this table';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.LOADED_LANDING_PAGE IS '{"comment":"This is a flag indicating whether the user loaded the US Stocks landing page on this particular date.","examples":[{"value":"1","explanation":"The user loaded the landing page"},{"value":"0","explanation":"The user did not load the landing page"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.LOADED_WATCHLIST_PAGE IS '{"comment":"This is a flag indicating whether the user loaded the watchlist page on this particular date.","examples":[{"value":"1","explanation":"The user loaded the watchlist page"},{"value":"0","explanation":"The user did not load the watchlist page"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FIRED_SEARCH IS '{"comment":"This is a flag indicating whether the user performed a search within the US Stocks section on this particular date.","examples":[{"value":"1","explanation":"The user performed a search"},{"value":"0","explanation":"The user did not perform a search"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.LOADED_COLLECTION_PAGE IS '{"comment":"This is a flag indicating whether the user loaded a collection page on this particular date.","examples":[{"value":"1","explanation":"The user loaded a collection page"},{"value":"0","explanation":"The user did not load a collection page"}]}';


COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.VISITED_STOCK_PAGE IS '{"comment":"This is a flag indicating whether the user visited any individual US stock details page on this particular date.","examples":[{"value":"1","explanation":"The user visited a stock details page"},{"value":"0","explanation":"The user did not visit any stock details page"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_LOADED_LANDING_PAGE IS '{"comment":"This represents the number of times the user loaded the US Stocks landing page on this particular date.","examples":["5","2","10"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_LOADED_WATCHLIST_PAGE IS '{"comment":"This represents the number of times the user loaded the watchlist page on this particular date.","examples":["3","1","7"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_FIRED_SEARCH IS '{"comment":"This represents the number of times the user performed a search within the US Stocks section on this particular date.","examples":["2","0","8"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_LOADED_COLLECTION_PAGE IS '{"comment":"This represents the number of times the user loaded a collection page on this particular date.","examples":["4","1","6"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_VISITED_STOCK_PAGE IS '{"comment":"This represents the number of times the user visited any individual stock page on this particular date.","examples":["6","2","12"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_VISITED IS '{"comment":"This is a comma-separated list of the distinct stock symbols the user visited on this particular date.","examples":[{"value":"AAPL,MSFT,GOOG","explanation":"User visited pages for Apple, Microsoft, and Google stocks"}, {"value":"TSLA,AMZN", "explanation":"User visited pages for Tesla and Amazon stocks"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_DISTINCT_STOCKS_VISITED IS '{"comment":"This represents the number of distinct stock symbols the user visited on this particular date.","examples":["3", "2", "5"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_TXNS IS '{"comment":"This represents the total number of wallet transactions (both add funds and withdraw funds) initiated by the user on this particular date.","examples":["2", "0", "4"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_ADD_FUND_TXNS IS '{"comment":"This represents the number of add funds transactions initiated by the user on this particular date.","examples":["1", "0", "3"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_WITHDRAW_FUND_TXNS IS '{"comment":"This represents the number of withdraw funds transactions initiated by the user on this particular date.","examples":["1", "0", "2"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_SUCCESS_TXNS IS '{"comment":"This represents the number of successful wallet transactions (both add funds and withdraw funds) completed by the user on this particular date. We typically use successful txn for querying and data analysis","examples":["2", "0", "3"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_ADD_FUND_SUCCESS_TXNS IS '{"comment":"This represents the number of successful add funds transactions completed by the user on this particular date. We typically use successful txn for querying and data analysis","examples":["1", "0", "2"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.ADD_FUND_SUCCESS_FLAG IS '{"comment":"This is a flag indicating whether the user had at least one successful add funds transaction on this particular date.","examples":[{"value":"1","explanation":"The user had at least one successful add funds transaction"},{"value":"0","explanation":"The user attempted a transaction but was not successful in adding funds"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.WITHDRAW_FUND_SUCCESS_FLAG IS '{"comment":"This is a flag indicating whether the user had at least one successful withdraw funds transaction on this particular date.","examples":[{"value":"1","explanation":"The user had at least one successful withdraw funds transaction"},{"value":"0","explanation":"The user attempted a withdraw funds transaction but it was not successful"},{"value":"null", "explanation":"The user did not attempt any withdraw funds transactions"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.ADD_FUND_FAILURE_FLAG IS '{"comment":"This is a flag indicating whether the user had at least one failed add funds transaction on this particular date.","examples":[{"value":"1","explanation":"The user had at least one failed add funds transaction"},{"value":"0","explanation":"The user did not have any failed add funds transactions"},{"value":"null", "explanation":"The user did not attempt any add funds transactions"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_WALLET_FUNDS_ADDED_USD IS '{"comment":"This represents the total amount of funds in USD successfully added to the users US Stocks broker wallet on this particular date.","examples":["100.00","500.50", "1000.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_WALLET_FUNDS_WITHDRAW_USD IS '{"comment":"This represents the total amount of funds in USD successfully withdrawn from the users US Stocks wallet on this particular date.","examples":["50.00","200.25", "500.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.AUM_DELTA_USD IS '{"comment":"This represents the change in the users Assets Under Management (AUM) in USD on this particular date. It reflects the net change due to wallet transactions and stock trades.","examples":["150.00", "-50.25", "200.75"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILED_ADD_FUND_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of failed add funds transactions initiated by the user on this particular date.","examples":["25.00", "0.00", "100.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.SUCCESS_ADD_FUND_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of successful add funds transactions completed by the user on this particular date.","examples":["75.00", "500.50", "900.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.CREATED_ADD_FUND_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of add funds transactions initiated by the user on this particular date, regardless of their success or failure status.","examples":["100.00", "500.50", "1000.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILURE_REASON_ADD_FUND IS '{"comment":"This column provides the reason for failure for add funds transactions, if applicable. It will be null if there are no failed add funds transactions for the user on this date.","examples":[{"value":"WALLET_ORDER_FAILURE_REASON_OUTWARD_SWIFT_TRANSFER_FAILED","explanation":"SWIFT transfer failed due to technical reasons or irregularities in forex."},{"value":"WALLET_ORDER_FAILURE_REASON_LRS_LIMIT_BREACHED","explanation":"Overall RBI limit for international remittance of $250,000 has been reached."},{"value":"WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_FOR_DAY","explanation":"Daily international remittance limit of 10L has been reached."},{"value":"WALLET_ORDER_FAILURE_REASON_PAN_CHECK_FAILED_WITH_BANKING_PARTNER","explanation":"Users PAN is ineligible for international remittances according to the bank; KYC actions are required."},{"value":"WALLET_ORDER_FAILURE_REASON_INSUFFICIENT_NO_OF_TRANSACTIONS","explanation":"Users bank account is not active enough and is considered risky."},{"value":"WALLET_ORDER_FAILURE_REASON_KYC_CHECK_FAILED_WITH_BANKING_PARTNER","explanation":"KYC check failed against the banking partner."},{"value":"WALLET_ORDER_FAILURE_REASON_FOREIGN_REMITTANCE_NOT_ALLOWED","explanation":"International remittances are not allowed for the user as per bank rejection."},{"value":"WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_IN_FINANCIAL_YEAR","explanation":"Regulatory limit set through suitability analysis has been breached."},{"value":"WALLET_ORDER_FAILURE_REASON_SOF_REMITTANCE_LIMIT_BREACHED","explanation":"Regulatory limit decided by the users Source of Funds document has been reached."},{"value":"null", "explanation":"No failed add funds transactions"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILED_WITHDRAW_FUND_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of failed withdraw funds transactions initiated by the user on this particular date. In case there is no withdraw amount failure for the user, then the value will be null","examples":["50.00", "10.00", "200.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.SUCCESS_WITHDRAW_FUND_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of successful withdraw funds transactions completed by the user on this particular date. In case theres no successful withdraw transaciton on that day for that user, the value will be null","examples":["20.00", "200.25", "300.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.CREATED_WITHDRAW_FUND_AMOUNT_USD IS '{"comment":"This represents the total amount in USD of withdraw funds transactions initiated by the user on this particular date, regardless of their success or failure status. This will be null in case there was no withdrawal attempted by the user on that day","examples":["50.00", "200.25", "500.00"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.FAILURE_REASON_WITHDRAW_FUND IS '{"comment":"This column provides the reason for failure for withdraw funds transactions, if applicable. Currently, only one failure reason is tracked: WALLET_ORDER_FAILURE_REASON_UNSPECIFIED. The value will be null if there are no failed withdraw funds transactions for the user on this date.","examples":[{"value":"WALLET_ORDER_FAILURE_REASON_UNSPECIFIED","explanation":"Unspecified reason for withdraw funds transaction failure."}, {"value":"null", "explanation":"No failed withdraw funds transactions"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_ORDERS IS '{"comment":"This represents the total number of US Stock buy or sell order attempts (both buy and sell) made by the user on this particular date, including canceled or failed orders. The value will be null if there are no order attempts made by the user on this date.","examples":["5", "10", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_BUY_ORDERS IS '{"comment":"This represents the total number of US Stock buy order attempts made by the user on this particular date, including canceled or failed orders. The value will be null if there are no buy order attempts made by the user on this date.","examples":["3", "7", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SELL_ORDERS IS '{"comment":"This represents the total number of US Stock sell order attempts made by the user on this particular date, including canceled or failed orders. The value will be null if there are no sell order attempts made by the user on this date.","examples":["2", "3", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SUCCESS_ORDERS IS '{"comment":"This represents the total number of successful US Stock orders (both buy and sell) placed by the user on this particular date. We typically use successful orders for querying and data analysis. The value will be null if there are no successful orders placed by the user on this date.","examples":["4", "8", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SUCCESS_BUY_ORDERS IS '{"comment":"This represents the total number of successful US Stock buy orders placed by the user on this particular date. We typically use successful orders for querying and data analysis. The value will be null if there are no successful buy orders placed by the user on this date.","examples":["2", "5", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_SUCCESS_SELL_ORDERS IS '{"comment":"This represents the total number of successful US Stock sell orders placed by the user on this particular date. We typically use successful orders for querying and data analysis. The value will be null if there are no successful sell orders placed by the user on this date.","examples":["2", "3", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_BUY_AMOUNT_USD IS '{"comment":"This represents the total value in USD of successful US Stock buy orders placed by the user on this particular date. The value will be null if there are no successful US Stock buy orders placed by the user on this date. ","examples":["2000.00", "5000.00", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.TOTAL_SELL_AMOUNT_USD IS '{"comment":"This represents the total value in USD of successful US Stock sell orders placed by the user on this particular date. The value will be null if there are no successful US Stock sell orders placed by the user on this date.","examples":["1500.00", "2500.00", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_TRADED IS '{"comment":"This is a comma-separated list of the distinct US stock symbols the user has placed a successful buy or sell order in on this particular date. The value will be null if there are no successful buy or sell order for the user on this date.","examples":[{"value":"AAPL,MSFT,GOOG","explanation":"User placed successful buy or sell order for Apple, Microsoft, and Google stocks"}, {"value":"TSLA,AMZN", "explanation":"User placed successful buy or sell order for Tesla and Amazon stocks"}, {"value":"null", "explanation":"User did not place any successful buy or sell order"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_BOUGHT IS '{"comment":"This represents the number of distinct US stock symbols the user successfully bought on this particular date. The value will be null if there are no successful US stock buy orders for the user on this date. ","examples":["3", "2", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.DISTINCT_STOCKS_SOLD IS '{"comment":"This represents the number of distinct US stock symbols the user successfully sold on this particular date. The value will be null if there are no successful US stock sell orders for the user on this date.","examples":["2", "1", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.NUM_WALLET_WITHDRAW_FUND_SUCCESS_TXNS IS '{"comment":"This represents the number of successful withdraw funds transactions completed by the user on this particular date. We typically use successful txn for querying and data analysis. The value will be null if the user did not attempt any withdraw funds transactions.","examples":["1", "2", "null"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY.WITHDRAW_FUND_FAILURE_FLAG IS '{"comment":"This is a flag indicating whether the user had at least one failed withdraw funds transaction on this particular date.","examples":[{"value":"1","explanation":"The user had at least one failed withdraw funds transaction"},{"value":"0","explanation":"The user did not have any failed withdraw funds transactions"},{"value":"null", "explanation":"The user did not attempt any withdraw funds transactions"}]}';"
""")


vn.train(ddl="""
"create or replace TRANSIENT TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS (
	TABLE_REFRESH_TIME TIMESTAMP_LTZ(9),
	WALLET_TRANSACTION_ID VARCHAR(16777216),
	ACTOR_ID VARCHAR(16777216),
	USS_ACCOUNT_ID VARCHAR(16777216),
	EXTERNAL_ACCOUNT_ID VARCHAR(16777216),
	CREATED_AT_IST TIMESTAMP_NTZ(9),
	CREATED_DATE_IST DATE,
	CREATED_WEEK_IST DATE,
	CREATED_MONTH_IST DATE,
	UPDATED_AT_IST TIMESTAMP_NTZ(9),
	UPDATED_DATE_IST DATE,
	UPDATED_WEEK_IST DATE,
	UPDATED_MONTH_IST DATE,
	DELETED_AT_IST TIMESTAMP_NTZ(9),
	STATUS VARCHAR(16777216),
	WALLET_ORDER_TYPE VARCHAR(16777216),
	WALLET_ORDER_TYPE_DERIVED VARCHAR(16777216),
	WALLET_ORDER_SUB_TYPE VARCHAR(16777216),
	FIRST_ADD_FUND_TIME_IST TIMESTAMP_NTZ(9),
	NEW_REPEAT_ADDFUND_USS VARCHAR(16777216),
	AMOUNT_INR FLOAT,
	AMOUNT_USD FLOAT,
	EXCHANGE_RATE NUMBER(38,6),
	LATEST_WF_STAGE VARCHAR(16777216),
	WF_REQ_ID VARCHAR(16777216),
	SWIFT_TXN_ID VARCHAR(16777216),
	POOL_TXN_ID VARCHAR(16777216),
	INVOICE_DETAILS VARCHAR(16777216),
	AMOUNT_REQUESTED_JSON VARCHAR(16777216),
	FAILURE_REASON VARCHAR(16777216),
	CLIENT_ORDER_ID VARCHAR(16777216),
	VENDOR_ORDER_ID VARCHAR(16777216),
	VENDOR_ACCOUNT_ID VARCHAR(16777216),
	EXTERNAL_ORDER_ID VARCHAR(16777216),
	PAYMENT_INFO VARCHAR(16777216),
	REMITTANCE_REQ_ID VARCHAR(16777216),
	WALLET_TXN_TIME_TAKEN_SEC NUMBER(18,0),
	WALLET_TXN_TIME_TAKEN_MINS NUMBER(18,0),
	WALLET_TXN_TIME_TAKEN_HOUR NUMBER(9,0),
	WALLET_TXN_TIME_TAKEN_DAYS NUMBER(9,0)
);

COMMENT ON TABLE EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS IS 'This table contains comprehensive information about Add Funds and Withdraw Funds transactions related to users US Stocks USD wallets. It tracks transaction details, timestamps, amounts in USD and INR, exchange rates, status, user identifiers, and more. This table is crucial for analyzing wallet transaction patterns, success rates, and user fund flow in and out of the USD wallets of the users with the vendor broker.';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.TABLE_REFRESH_TIME IS '{"comment":"This represents the timestamp when the table was last refreshed.","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TRANSACTION_ID IS '{"comment":"This is the unique identifier for a wallet transaction, serving as the primary key for this table. It is used to track individual add funds or withdraw funds requests.","examples":["USSWO4EzRQvpHyC240716", "USSWO3tczkdvSUb240718", "USSWO3AXf76p19y240712"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.ACTOR_ID IS '{"comment":"This is the identifier for a user across the organization. It represents the user who initiated the wallet transaction and can be used as a joining key to connect with user data in other tables.","examples":["738a1cc8-0efa-4432-aa36-c4dda7627268", "25468f79-ed7e-4488-a8d8-ccd307d2a2f3", "ebe7ce8b-2e88-49c2-bfe3-b56980bff58a"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.USS_ACCOUNT_ID IS '{"comment":"This is the unique identifier for a users US Stocks brokerage account which is opened with the vendor. It represents the account associated with the wallet transaction.","examples":["USSACCpp3AQIkLSTutA0M6dEsT8A240702==", "USSACCcnkiV/oCQyGw00obg4UU6A240719==", "USSACCJrPSNrQkTVWWq40uXM+UgA240331=="]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.EXTERNAL_ACCOUNT_ID IS '{"comment":"This is the account_id but shown to external users in a relatively more readable format. It is a counterpart to USS Account ID. It is not that important of a column.","examples":["363ab2aa4507344bbcecec1dcdb2896b870b3cbc6ca7a7725d694b1e87c810a6", "1cfe2ca413e8fd7a0ef3eaede99e3b6c1bdb3b5e180dab0ae753431f507fa096"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_AT_IST IS '{"comment":"This timestamp indicates when the wallet transaction was created in IST (Indian Standard Time). It captures the precise moment the transaction request was initiated.","examples":"2024-07-19 09:46:09.960"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_DATE_IST IS '{"comment":"This field represents the date in IST when the wallet transaction was created. This column is frequently used for aggregating wallet transactions on a daily basis. It is generally the most reliable column for conducting any form of analysis on wallet transactions.","examples":"2024-07-19"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_WEEK_IST IS '{"comment":"This date field signifies the start of the week in IST during which the wallet transaction was created. It allows for analysis of wallet transaction trends or patterns on a weekly basis. ","examples":"2024-07-15"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CREATED_MONTH_IST IS '{"comment":"This date field indicates the beginning of the month in IST when the wallet transaction was created. It is useful for tracking monthly transaction volumes or other month-over-month analyses.","examples":"2024-07-01"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_AT_IST IS '{"comment":"This timestamp field records the most recent update to the wallet transaction in IST. It captures the time of any status changes, modifications, or other relevant events related to the transaction.","examples":"2024-07-19 19:02:25.052"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_DATE_IST IS '{"comment":"This field represents the date in IST when the wallet transaction was most recently updated. It is often used to track the recency of changes or actions on the transaction.","examples":"2024-07-19"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_WEEK_IST IS '{"comment":"This date field signifies the start of the week in IST during which the wallet transaction was last updated. ","examples":"2024-07-15"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.UPDATED_MONTH_IST IS '{"comment":"This date field indicates the beginning of the month in IST when the wallet transaction was last updated. ","examples":"2024-07-01"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.DELETED_AT_IST IS '{"comment":"This timestamp field indicates when the wallet transaction was soft deleted in IST, if applicable.  A non-null value suggests the transaction was removed or canceled at some point. It will be null if the wallet order is not deleted. ","examples":"2024-07-19 19:02:25.052"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.STATUS IS '{"comment":"This field indicates the current status of the wallet order.","examples":[{"value":"WALLET_ORDER_STATUS_CREATED","explanation":"The wallet order has been created successfully but is not yet fully processed."},{"value":"WALLET_ORDER_STATUS_FAILED","explanation":"The wallet order failed due to some reason."},{"value":"WALLET_ORDER_STATUS_SUCCESS","explanation":"The wallet order has been successfully completed."},{"value":"WALLET_ORDER_STATUS_MANUAL_INTERVENTION","explanation":"The wallet order requires manual intervention and debugging by an engineer due to a technical issue."},{"value":"WALLET_ORDER_STATUS_INITIATION_FAILED","explanation":"The wallet order initiation failed."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_ORDER_TYPE IS '{"comment":"This field specifies the type of wallet order initiated by the user.","examples":[{"value":"WALLET_ORDER_TYPE_ADD_FUNDS","explanation":"User initiated an international transaction to add funds to their USD wallet from their Indian bank account."},{"value":"WALLET_ORDER_TYPE_WITHDRAW_FUNDS","explanation":"User initiated an international transaction to withdraw funds from their USD wallet back to their Indian bank account."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_ORDER_TYPE_DERIVED IS '{"comment":"This is a cleaner, more readable version of the 'WALLET_ORDER_TYPE' column. It provides a user-friendly representation of the wallet order type.","examples":[{"value":"Add Funds","explanation":"Represents an add funds wallet transaction"}, {"value":"Withdraw Funds","explanation":"Represents a withdraw funds wallet transaction"}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_ORDER_SUB_TYPE IS '{"comment":"This field provides a more granular classification of the wallet order type.","examples":[{"value":"WALLET_ORDER_SUB_TYPE_UNSPECIFIED","explanation":"Used for older wallet orders; can generally be ignored."},{"value":"WALLET_ORDER_SUB_TYPE_ADD_FUNDS_REWARDS","explanation":"Represents a reward credit added to the users wallet automatically by Epifi."},{"value":"WALLET_ORDER_SUB_TYPE_NON_INSTANT_WALLET_WITHDRAWAL","explanation":"Represents a standard withdrawal transaction from the users wallet."}, {"value":"WALLET_ORDER_SUB_TYPE_ADD_FUNDS_NON_INSTANT_WALLET_FUNDING","explanation":"Represents a standard add funds transaction to the users wallet."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.FIRST_ADD_FUND_TIME_IST IS '{"comment":"This timestamp captures the time in IST when the user made their very first successful 'Add Funds' transaction to their US Stocks wallet. This is a user-level attribute, not specific to individual wallet orders.","examples":"2024-06-18T20:58:38.156Z"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.NEW_REPEAT_ADDFUND_USS IS '{"comment":"This field categorizes the user\'s wallet transaction based on whether it is their first ever user-initiated wallet transaction (excluding any previous reward transactions credited by the organization).","examples":[{"value":"New","explanation":"This is the user\'s first wallet transaction initiated by them (excluding reward transactions)."},{"value":"Repeat","explanation":"The user has made wallet transactions before (excluding reward transactions)."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.LATEST_WF_STAGE IS '{"comment":"This field represents the most recent stage of the workflow associated with processing the wallet transaction. Workflows vary depending on the transaction type (Add Funds, Withdraw Funds, Reward).","examples":[{"value":"TRACK_ORDER", "explanation":"For Reward transactions: System is monitoring whether the reward amount has been credited."}, {"value":"SEND_BUY_ORDER", "explanation":"For Reward transactions: Subsequent buy order request sent after reward amount credit."}, {"value":"TRACK_WALLET_FUND_TRANSFER", "explanation":"For Add Funds transactions: System is tracking the international transfer and crediting to the users wallet."}, {"value":"REFUND_PAYMENT", "explanation":"For Add Funds transactions: Initiating or completing a refund due to a failed foreign funds transfer."}, {"value":"POOL_ACCOUNT_TRANSFER", "explanation":"For Add Funds transactions: Users payment has been credited to the banks pool account."}, {"value":"FOREIGN_FUND_TRANSFER", "explanation":"For Add Funds transactions: Bank-initiated international transfer is in progress."}, {"value":"TRACK_INWARDS_REMITTANCE_STATUS", "explanation":"For Withdraw Funds transactions: Tracking the inward remittance of the withdrawal."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.AMOUNT_INR IS '{"comment":"This field represents the transaction amount in INR (Indian Rupees). It applies to both Add Funds and Withdraw Funds transactions.","examples":"2120.75"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.AMOUNT_USD IS '{"comment":"This field represents the transaction amount in USD (US Dollars). It applies to both Add Funds and Withdraw Funds transactions.","examples":"25"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.EXCHANGE_RATE IS '{"comment":"This field indicates the USD/INR exchange rate used for the wallet transaction. The exchange rate is determined and can be updated during order processing but is fixed upon successful order completion. It will be the Buy exchange rate for Add Funds transactions and the Sell exchange rate for Withdraw Funds transactions.","examples":"84.830000"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WF_REQ_ID IS '{"comment":"This is a unique identifier for the workflow responsible for orchestrating the wallet order at the backend. It is used for tracking and managing the different stages of the wallet transaction process.","examples":["WFRnH947AL0SW20JA6eHApLWw240719==", "WFRXqazdYL+Tj6vdMHo7x8fzQ240719=="]}';

OMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.SWIFT_TXN_ID IS '{"comment":"This field contains the SWIFT (International transaction) ID associated with the wallet transaction.  It is only present for Add Funds transactions and will be null for other types. Note that this ID is not unique, as multiple transactions might be mapped to a single SWIFT.","examples":"5555FOTT33124"}'; 

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.POOL_TXN_ID IS '{"comment":"This field stores the unique identifier for the payment transaction associated with the transfer to the pool account. It is primarily relevant for Add Funds transactions.","examples":["117a4dc90d8158030aee170c99be934d594eae067e885a4a091491bf2d9fc56a", "68b0e89486fa9f7b7441bc5f72af777226ba6fb87e008b6a6eee5c657d17c011"]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.INVOICE_DETAILS IS '{"comment":"This field stores invoice details that are presented to the user in JSON format. It includes information like GST, TCS, amounts in INR and USD, the applied forex rate, and more.  This JSON structure needs to be unmarshalled to access specific fields.","examples":[{"value":"{\\"GST\\": {\\"units\\": \\"45\\", \\"currencyCode\\": \\"INR\\"}, \\"TCS\\": {\\"currencyCode\\": \\"INR\\"}, \\"amountInInr\\": {\\"nanos\\": 500000000, \\"units\\": \\"12724\\", \\"currencyCode\\": \\"INR\\"}, \\"amountInUSD\\": {\\"units\\": \\"150\\", \\"currencyCode\\": \\"USD\\"}, \\"forexRateId\\": \\"FXwIodSqeFQn2QFM8obeMwzg240718==\\", \\"totalDebitAmount\\": {\\"nanos\\": 500000000, \\"units\\": \\"12769\\", \\"currencyCode\\": \\"INR\\"}, \\"forexRateProvenance\\": \\"FOREX_RATE_PROVENANCE_MANUAL_PURCHASE\\", \\"partnerExchangeRate\\": {\\"nanos\\": 830000000, \\"units\\": \\"84\\", \\"currencyCode\\": \\"INR\\"}}", "explanation":"Example JSON structure containing invoice details. Key fields include: GST (amount and currency), TCS (currency), amountInInr, amountInUSD, forexRateId, totalDebitAmount, forexRateProvenance, partnerExchangeRate"}]}'; 

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.AMOUNT_REQUESTED_JSON IS '{"comment":"This field stores the originally requested transaction amount and currency in JSON format. The JSON needs to be unmarshalled to extract the amount and currency information.","examples":[{"value":"{\\"units\\": 150, \\"currency_code\\": \\"USD\\"}", "explanation":"Example JSON showing the requested amount (150) and currency (USD)."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.FAILURE_REASON IS '{"comment":"This field provides the reason for failure of the wallet order, if applicable. It will be null for successful orders.","examples":[
{"value":"WALLET_ORDER_FAILURE_REASON_KYC_CHECK_FAILED_WITH_BANKING_PARTNER", "explanation":"KYC check failed with the banking partner."},
{"value":"WALLET_ORDER_FAILURE_REASON_SOF_REMITTANCE_LIMIT_BREACHED", "explanation":"Source of Funds remittance limit has been exceeded."}, 
{"value":"WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_IN_FINANCIAL_YEAR", "explanation":"Maximum allowed limit for adding funds in the financial year has been reached."}, 
{"value":"WALLET_ORDER_FAILURE_REASON_LRS_LIMIT_BREACHED", "explanation":"Liberalised Remittance Scheme (LRS) limit has been exceeded."},
{"value":"WALLET_ORDER_FAILURE_REASON_FOREIGN_REMITTANCE_NOT_ALLOWED", "explanation":"Foreign remittance is not allowed for the user based on bank or regulatory restrictions."}, 
{"value":"WALLET_ORDER_FAILURE_REASON_PAN_CHECK_FAILED_WITH_BANKING_PARTNER", "explanation":"PAN card check failed with the banking partner."},
{"value":"WALLET_ORDER_FAILURE_REASON_INSUFFICIENT_NO_OF_TRANSACTIONS", "explanation":"The users bank account has insufficient transaction history and is considered risky."}, 
{"value":"WALLET_ORDER_FAILURE_REASON_BREACHED_MAX_ALLOWED_LIMIT_TO_ADDED_FUNDS_FOR_DAY", "explanation":"Maximum allowed limit for adding funds in a day has been reached."},
{"value":"WALLET_ORDER_FAILURE_REASON_UNSPECIFIED", "explanation":"Unspecified reason for failure."}, 
{"value":"WALLET_ORDER_FAILURE_REASON_ERROR_TRANSFERRING_AMOUNT_TO_POOL_ACCOUNT", "explanation":"Error transferring the amount to the pool account."}, 
{"value":"WALLET_ORDER_FAILURE_REASON_OUTWARD_SWIFT_TRANSFER_FAILED", "explanation":"The outward SWIFT transfer failed."},
{"value":"WALLET_ORDER_FAILURE_REASON_UNSPECIFIED", "explanation":"Unspecified reason for withdraw funds transaction failure."}, 
{"value": null, "explanation": "No failure reason. Order was successful."}
]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.CLIENT_ORDER_ID IS '{"comment":" This is the order ID which is sometimes used for debugging anything on Android or iOS clients. ","examples":"325968ea-6007-47f6-bdf5-2f172f60b316"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.VENDOR_ACCOUNT_ID IS '{"comment":"This is a unique identifier for the users account on the vendor broker's platform. It is used to track and manage the user's funds and transactions with the vendor.","examples":"d7d1ad8acc6892f36539aac0a9319f656aa079cd3963699e9fe16fc9051ee975"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.EXTERNAL_ORDER_ID IS '{"comment":"This is an order ID that is exposed externally to users, often for reference on invoices or during support interactions.","examples":"BS5XFMsDnf1p"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.VENDOR_ORDER_ID IS '{"comment":"This is the unique identifier assigned to the wallet order by the vendor or payment processor. It is used for reconciliation and tracking transactions on the vendors side.","examples":"ab7e62aa-90c9-47d0-8403-c0f06cf8a782"}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.PAYMENT_INFO IS '{"comment":"This field provides additional payment-related information in JSON format, which may vary depending on the payment method used.","examples":[{"value":"{\\"utrNumber\\": \\"S10836315\\"}", "explanation":"Example JSON structure containing payment info. In this case, it includes the UTR (Unique Transaction Reference) number."}]}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_SEC IS '{"comment":"This field measures the total time taken for the wallet transaction to complete, expressed in seconds. It represents the duration from order creation to successful completion (or failure).","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_MINS IS '{"comment":"This field measures the total time taken for the wallet transaction to complete, expressed in minutes. It represents the duration from order creation to successful completion (or failure).","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_HOUR IS '{"comment":"This field measures the total time taken for the wallet transaction to complete, expressed in hours. It represents the duration from order creation to successful completion (or failure).","examples":""}';

COMMENT ON COLUMN EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS.WALLET_TXN_TIME_TAKEN_DAYS IS '{"comment":"This field measures the total time taken for the wallet transaction to complete, expressed in days. It represents the duration from order creation to successful completion (or failure).","examples":""}';"
""")

vn.train(ddl="""
"create or replace TABLE EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS (
	CHANNEL VARCHAR(16777216),
	EVENT VARCHAR(16777216),
	INTEGRATIONS VARCHAR(16777216),
	META VARCHAR(16777216),
	ORIGINALTIMESTAMP VARCHAR(16777216),
	PROPERTIES VARCHAR(16777216),
	RECEIVEDAT VARCHAR(16777216),
	SENTAT VARCHAR(16777216),
	TIMESTAMP TIMESTAMP_NTZ(9),
	TYPE VARCHAR(16777216),
	ACTOR_ID VARCHAR(16777216),
	APP VARCHAR(16777216),
	MANUFACTURER VARCHAR(16777216),
	MODEL VARCHAR(16777216),
	NETWORK VARCHAR(16777216),
	OS VARCHAR(16777216),
	EVENT_ID VARCHAR(16777216),
	EVENT_SOURCE VARCHAR(16777216),
	SCREEN_NAME VARCHAR(16777216),
	SESSION_ID VARCHAR(16777216),
	TIMESTAMP_IST TIMESTAMP_NTZ(9),
	FAILURE_REASON VARCHAR(16777216),
	PARTITION_COLUMN VARCHAR(16777216)
);

COMMENT ON COLUMN EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.EVENT IS  '{"comment":"This field represents the name of the event","examples":["USSPreLaunchScreenLoad","USSClickSort","USSDetailsPageExited"]}';
COMMENT ON COLUMN EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.TIMESTAMP IS  '{"comment":"This field represents the exact time at which the time was fired","examples":"2023-05-24 08:57:31.696"}';
COMMENT ON COLUMN EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.ACTOR_ID IS  '{ "comment": "It is the identifier for a user across the organisation. This is a data point present across most tables in the organisation where there is a user action. Should be used as a joining key, since it represents the user identifier.","examples": ["35479187-1a5a-4dd2-80fd-695c2eb3f657","20188659-94f0-46b2-bfb8-a3bdb3605f0d","7b62cbda-a73f-4768-aa42-deced1ceaf5e"]}';
COMMENT ON COLUMN EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS.PROPERTIES IS  '{ "comment": "It has the properties for the events in JSON form. The JSON will need to be unmarshalled to check all the properties. Refer to document related to check exact event and property required","examples": "{"entry_point":"HOME_SMART_DEPOSIT_TAB","entry_point_v2":"HOME_SMART_DEPOSIT_TAB","event_id":"2d89d837-6224-42c1-bac4-8bb1e52e6af9","funnel_start":","opted_in":"true","screen_name":"default","session_id":"605b15d6-1628-415a-9fdc-ce25ad523bb3","timestamp":"1684918651696"}"}';
""")