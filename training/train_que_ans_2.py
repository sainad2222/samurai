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

vn.train(question="""how many stocks has actor 'A' bought ever? what are those stocks?""", sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. From this table we need the number of distinct stocks purchased and list of distinct stocks bought


select num_distinct_stocks_bought_ever, distinct_stocks_bought_ever 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where 1=1
    and actor_id = 'A'""")

vn.train(question="""I want to see monthwise total add fund transactions and amount for different add fund cohorts. First add fund month will be the cohort of the actor. For example my first add fund transaction was on 3rd jan 2024 I will be in Jan 2024 Cohort""", sql="""-- We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY A which has daily activity data of a user.This data is at an actor day level from this table we are extracting activity month, activity date and  number of wallet add fund transactions
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
group by 1,2;""")
vn.train(question="""I need all need all the actor_ids and their moengage id of USS broker account holders """, sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table.  From this table we need account status of an actor and account status
-- We are joining USS_USER_BASE_FACT and EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B to get Moengage IDs. firehose_id in this table is actor_id in all USS tables. This table has one row per firehose_id (actor_id) 

-- we have applied account_status = 'ACTIVE' filter to filter in only USS broker account holders
-- we have selected actor_Id and firehose id as requried in the code
select actor_id, moengage_id
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT O
left join   EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS VM
   on O.actor_id= VM. firehose_id
where account_status = 'ACTIVE';""")
vn.train(question="""I want data of all users who have churned from US stock . I want to see all the stocks they purchased

We consider a user as churned if they have added greater than 15$ in their first add fund and their current AUM in less than 5$""", sql="""-- we are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. We need USS_USER_BASE_FACT to get the first success add fund amount and AUM USD, account status
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
    and AUM_USD < 5;""")
vn.train(question="""I want the count of different users in different add fund cohorts. First add fund month will be the cohort of the actor. For example my first add fund transaction was on 3rd jan 2024 I will be in Jan 2024 Cohort""", sql="""-- we are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. 

-- date_trunc(month, B.first_success_add_fund_date) is a function used to extract month from date
select date_trunc(month, B.first_success_add_fund_date) as first_add_fund_month, count(distinct B.actor_id) as total_actors
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT B
where 1=1
    and B.first_success_add_fund_date >= '2024-01-01'
group by 1;""")
vn.train(question="""I want actor ids and moengage ids of all actors who are invested in Nvidia""", sql="""-- this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here
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
where active_qty > 0;""")
vn.train(question="""Give me the stock ids of the following stocks 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'?
tell me about these stock symbols 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'.
are these stock ids active? 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'.""", sql="""-- We have used used EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS. This table contains all the stock level details. one row per stock. Contains details of Stocks and ETFs both

-- Its good to display internal_status, stock_type in such queries. these are good to know details of each stock
select Symbol, ID as stock_id  , internal_status, stock_type    
from EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS where symbol in ('BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM')
;""")
vn.train(question="""I want to see all the Wallet transactions in the last 7 weeks. Want to see User ID, Transaction_ID, time_stamp, order_type, status, amount , vendor account id. also need some user information like lifetime total add funds, Account creation date, first add fund date, last add fund date""", sql="""-- we have used 
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
    and W. created_date_ist >= current_date() - 6 ;""")
vn.train(question="""I want to see all the Stock orders in last 7 days, Need the below information Actor_id, Transaction ID, order type, Status , Transaction Date , transaction amount , quantity, Stock symbol""", sql="""-- we have used  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here


select Actor_id, Txn_ID, Type, Txn_Status, TXN_CREATED_DATE, TXN_AMOUNT_CONFIRMED_USD, QTY_CONFIRMED, STOCK_SYMBOL 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where txn_created_date >= current_date() - 6;""")
vn.train(question="""I want D0, D7, D14, D30 and D365 Activation Rate/ Add Fund rate . Activation means first wallet add funds ever""", sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. From this table we need the account creation date and first successful add fund date
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
order by 1;""")
vn.train(question="""Give details of about wallet transaction of a customer. need     ACTOR_ID,Transaction id,time to complete transaction in minutes,
    transaction timestamp,
    amount of transaction, transaction type""", sql="""-- We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS. this table contains all wallet orders (or transactions)


SELECT 
    ACTOR_ID,
    WALLET_TRANSACTION_ID,
    WALLET_TXN_TIME_TAKEN_MINS,
    CREATED_AT_IST,
    AMOUNT_USD
    ROW_NUMBER() OVER (PARTITION BY ACTOR_ID ORDER BY CREATED_AT_IST ASC) AS rn
FROM EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS
qualify rn =1;""")
vn.train(question="""I need all need all the actor_ids and their moengage id of USS broker account holders who have not added funds yet""", sql="""-- We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table.  From this table we need account status of an actor and first success_add_funds of an actor
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
    and first_success_add_fund_date is null""")
vn.train(question="""How many users bought the following stocks in the last 7 days and how amny transactions occured?
('NEM','IAU','GOLD','AAAU','FNV','GFI','AEM','GDX','AU')   """, sql="""-- we have used  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here
-- we have applied filter on stock_symbol column to filter in listed stocks
-- date filter is also applied to filter out last 7 days

select txn_created_date , count(*) as txns
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS A
where type = 'BUY'
    and stock_symbol in ('NEM','IAU','GOLD','AAAU','FNV','GFI','AEM','GDX','AU')   
    and txn_created_date >= current_date() - 6
group by 1
order by 1;""")
vn.train(question="""I want to see the monthly total add funds, total withdraw funds and the difference between them from January 1st 2024 onwards.""", sql="""-- EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY which has daily activity data of a user. This data is at an actor day level. From this table we are extracting activity month, activity date, and number of wallet add fund amount and wallet withdraw amount
we have applied filters to select the actors whose activity is from January 1st 2024 and onwards
we use date_trunc(month, created_date_ist) to extract month from date we have used sum(total_wallet_funds_added_usd) to extract the total funds added in a month, sum(total_wallet_funds_withdraw_usd) to extract total funds withdrawn in a month.
select date_trunc(month, created_date_ist) as mth, sum(total_wallet_funds_added_usd) as Add_funds, sum(total_wallet_funds_withdraw_usd) as WithdRAW_FUNDS, coalesce(Add_funds,0) - coalesce(WithdRAW_FUNDS,0) as total_wallet_funds_withdraw_usd from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY where 1=1 and created_date_ist >= '2024-01-01' group by 1;""")
vn.train(question="""I want to see the daily churn count for users who had an AUM of 15 USD or greater the previous day and whose AUM fell below 15 USD on the current day, for users who added at least 15 USD total add fund transaction and who have activity starting from January 1st 2024 onwards.""", sql="""-- EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY which has daily activity data of a user. This data is at an actor day level. We are extracting AUM delta from this table (AUM_DELTA_USD) which gives the change in AUM on each activity day. We also extract the CREATED_DATE_IST and ACTOR_ID. These are essential for calculating cumulative AUM (using the window function) and determining daily churn. We also join it with EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT. This is a user level table to get the total_wallet_funds_added_usd which is used to filter for users who have added at least 15 USD in total.
-- we have applied filters to select the actors for whom who added fund post jan 1st B. total wallert add funds amount >= 15 and for actors whose activity is from January 1st 2024 and onwards
we use sum(coalesce(AUM_DELTA_USD,0)) over(partition by A. actor_id order by CREATED_DATE_IST rows between unbounded preceding and current row ) as AUM to calculate cumulative AUM by user from the first day of their activity, we use lag(AUM) over(partition by actor_id order by created_date_ist ) as prev_day_AUM to calculate previous day AUM for the user. Finally, we use count(distinct case when prev_day_AUM >= 15 and AUM < 15 then actor_id end) as churn to identify users whose AUM has dropped below 15 from being above 15 on the previous day
select CREATED_DATE_IST,
count(distinct case when prev_day_AUM >= 15 and AUM < 15 then actor_id end) as churn
from
(select *, lag(AUM) over(partition by actor_id order by created_date_ist ) as prev_day_AUM
from
(
select A.actor_id, A.CREATED_DATE_IST, sum(coalesce(AUM_DELTA_USD,0)) over(partition by A. actor_id order by CREATED_DATE_IST rows between unbounded preceding and current row ) as AUM
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY A
left join
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT B
on A. actor_id = B. actor_id
where 1 = 1
and B. total_wallet_funds_added_usd >= 15
and CREATED_DATE_IST >= '2024-01-01'
))
group by 1""")
vn.train(question="""I need all distinct user ids and their associated moengage_ids of users who visited USS in last 30 days""", sql="""-- EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A which has user events data related to US stocks. This table has actor_id, timestamp_ist, event, and other columns related to events. We join it with EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS to get the moengage id
-- we have applied filters to select the actors whose activity is from last 30 days and onwards and have visited USS. These are the events which signify US Stock visit ('USSLandingPageLoad','USSCollectionPageload','USSDetailsPageLoaded')
-- we use distinct actor_id, moengage_id to extract unique actor_id and moengage_id who have performed any of the events
select 
    distinct actor_id, moengage_id
from EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A
left join 
 EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B
on A. actor_id = B. firehose_id
where 1= 1
    and date(timestamp_ist) >= current_date() -30
    -- and date(timestamp_ist) < current_date()
    and event in ('USSLandingPageLoad','USSCollectionPageload','USSDetailsPageLoaded')""")
vn.train(question=""" I need all distinct actor_ids who have visited the ETF stock page last 6 days.
""", sql="""-- EPIFI_DATALAKE_ALPACA.EVENTS.USS_INVEST_SERVER_EVENTS which has server events data related to US stocks. This table has actor_id, timestamp_ist, event, and other columns related to events. We extract the stock_id from the properties column using parse_json(properties):stock_id and join it with EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS which has details of stocks and ETFs
-- we have applied filters to select the actors who have visited stock page (Event for stock page visit is 'USSDetailsPageLoadedServer') and whose activity is from last 6 days and onwards. We also filter the stocks based on stock_type = 'STOCK_TYPE_ETF' to filter inly ETF page visits
-- we use distinct actor_id to extract unique actor_id who have visited the Stock page of an ETF stock in the past 6 days
        (select Distinct Actor_id
        from
        (select actor_id, parse_json(properties):stock_id as stock_id
        from EPIFI_DATALAKE_ALPACA.EVENTS.USS_INVEST_SERVER_EVENTS
        where 1=1
            and event = 'USSDetailsPageLoadedServer'
            -- and parse_json(properties):stock_id
            and date( timestamp_ist) >= current_date() - 6
        group by 1,2) A
        inner join
        (select id as stock_id
        From EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS
        where 1=1
            and stock_type = 'STOCK_TYPE_ETF') B
        on A. stock_id  = B. stock_id)""")
vn.train(question="""What is the average amount of successful "Add Funds" wallet transactions in the past 30 days? / What is the average add fund amount in last 30 days""", sql="""-- EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS which contains all the wallet transactions data. We are extracting the amount_usd from this table
-- we have applied filters to select the actors whose wallet_order_type_derived is 'Add Funds'  to filter Add fund transactions only and status is 'WALLET_ORDER_STATUS_SUCCESS' to filter success transctions only and whose activity is from last 30 days and onwards
 we use avg(amount_usd) to calculate the average add funds amount in the past 30 days
select avg(amount_usd)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS
where wallet_order_type_derived = 'Add Funds'
and status = 'WALLET_ORDER_STATUS_SUCCESS'
and created_date_ist >= current_date() -30;""")
vn.train(question="""What is the minimum amount of the first successful add funds transaction for users who added funds on the same day they created their accounts?""", sql="""-- EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT which is a user level table. From this table we extract the first_success_add_fund_amt_usd column
-- we have applied filters to select the actors whose account creation date is the same as their first successful add funds date
-- we use min(first_success_add_fund_amt_usd) to calculate the minimum first successful add funds amount for users who added funds on the same day they created their accounts.
select min(first_success_add_fund_amt_usd)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where acct_creation_date_ist = first_success_add_fund_date
and 1=1;""")
vn.train(question="""I want daywise USS account creation starters. Events of Account creation starters are 
('USSSetUpAccountBottomSheetload',
                'USSCreateProfileScreenLoaded',
                'USSCollectRiskLevelScreenLoaded',
                'USSDocumentsSubmissionInfoScreenload',
                'USSDisclaimerDetailsPageload',
                'USSPANUploadScreenload',
                'USSPANValidationTerminalScreenload',
                'USSSourceOfFundsScreenload',
                'USSEmployerDetailsScreenload')""", sql="""-- EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A which has user events data related to US stocks. This table has actor_id, timestamp_ist, event, and other columns related to events.
-- we have applied filters to select the actors whose event is in the list of events mentioned in the events column which are valid for account creation starters and whose activity is from Feb 1st 2024 and till yesterday's date
-- we use date(timestamp_ist) as DATE1 to extract the date from timestamp_ist and count(distinct actor_id) as ACTORS to count the distinct actor ids who performed the event
select date(timestamp_ist) as DATE1, count(distinct actor_id) as ACTORS
from EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A
where 1=1
    and event in (                    
                'USSSetUpAccountBottomSheetload',
                'USSCreateProfileScreenLoaded',
                'USSCollectRiskLevelScreenLoaded',
                'USSDocumentsSubmissionInfoScreenload',
                'USSDisclaimerDetailsPageload',
                'USSPANUploadScreenload',
                'USSPANValidationTerminalScreenload',
                'USSSourceOfFundsScreenload',
                'USSEmployerDetailsScreenload'
                            )
    and date(timestamp_ist) >= '2024-02-01'
    and date(timestamp_ist) <= current_date()-1
group by 1
order by 1; """)
vn.train(question="""I want to see the daily count of account creations feb 1st onwards""", sql="""-- EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT which is a user level table. We are extracting the acct_creation_date_ist and actor_id from this table
-- we have applied filters to select the actors whose account status is 'ACTIVE' and whose account creation date is from Feb 1st 2024 and till yesterday's date
-- we use acct_creation_date_ist to extract the account creation date and count(distinct actor_id) to count the number of distinct actors who created their accounts on that date
select acct_creation_date_ist, count(distinct actor_id)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where ACCOUNT_STATUS = 'ACTIVE'
    and acct_creation_date_ist >= '2024-02-01'
    and acct_creation_date_ist <= current_date()-1
group by 1;    """)
vn.train(question="""I want to see day wise Activations in last 30 days / I want to see the daily count of distinct actors who have performed their first successful "Add Funds" wallet transaction in the past 30 days.""", sql="""-- EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS W which contains all the wallet transactions data. We are extracting the created_date_ist and actor_id from this table. We also extract NEW_REPEAT_ADDFUND_USS 
-- we have applied filters to select the actors whose wallet_order_type_derived is 'Add Funds' and whose NEW_REPEAT_ADDFUND_USS is 'New' to filter in only first time add fund actors. activations new actors adding funds. mean and status is 'WALLET_ORDER_STATUS_SUCCESS' and whose activity is from last 30 days and onwards
-- we use created_date_ist to extract the date and count(distinct actor_id) as activations to count the number of distinct actors who have performed their first successful add funds transaction in the past 30 days.
select created_date_ist, count(distinct actor_id) as activations
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS W
where 1=1
    and wallet_order_type_derived = 'Add Funds'
    and NEW_REPEAT_ADDFUND_USS = 'New'
    and status = 'WALLET_ORDER_STATUS_SUCCESS'
    and created_date_ist >= current_date() -30
    ;""")