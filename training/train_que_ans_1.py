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
    question="""how many stocks has actor 'A' bought ever? what are those stocks?""",
    sql="""/* We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. From this table we need the number of distinct stocks purchased and list of distinct stocks bought

*/
select num_distinct_stocks_bought_ever, distinct_stocks_bought_ever 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where 1=1
    and actor_id = 'A'""",
)
vn.train(
    question="""I want to see monthwise total add fund transactions and amount for different add fund cohorts. First add fund month will be the cohort of the actor. For example my first add fund transaction was on 3rd jan 2024 I will be in Jan 2024 Cohort""",
    sql="""/* We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY A which has daily activity data of a user.This data is at an actor day level from this table we are extracting activity month, activity date and  number of wallet add fund transactions
 Its joined with EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT. This is a user level table.  to get first add fund month
 we have applied filters to select the actors for whom who added fund post jan 1st
B.first_success_add_fund_date >= '20240101'
 we use date_trunc(month, B.first_success_add_fund_date)  to extract month from date */
select  date_trunc(month, B.first_success_add_fund_date) as first_add_fund_month, 
        date_trunc(month, A.created_date_ist) as txn_month,
        sum(coalesce(A. num_wallet_add_fund_success_txns,0) ) as num_add_fund_txns,
        sum(coalesce(A. total_wallet_funds_added_usd,0)) as Total_Funds_added 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY A
left join 
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT B
on A. actor_id = B. actor_id
and A. created_date_ist >= B. first_success_add_fund_date
where B.first_success_add_fund_date >= '20240101'
group by 1,2;""",
)
vn.train(
    question="""I need all need all the actor_ids and their moengage id of USS broker account holders """,
    sql="""/* We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table.  From this table we need account status of an actor and account status
 We are joining USS_USER_BASE_FACT and EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B to get Moengage IDs. firehose_id in this table is actor_id in all USS tables. This table has one row per firehose_id (actor_id) 

 we have applied account_status = 'ACTIVE' filter to filter in only USS broker account holders
 we have selected actor_Id and firehose id as requried in the code*/
select actor_id, moengage_id
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT O
left join   EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS VM
   on O.actor_id= VM. firehose_id
where account_status = 'ACTIVE';""",
)
vn.train(
    question="""I want data of all users who have churned from US stock . I want to see all the stocks they purchased

We consider a user as churned if they have added greater than 15$ in their first add fund and their current AUM in less than 5$""",
    sql="""/* we are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. We need USS_USER_BASE_FACT to get the first success add fund amount and AUM USD, account status
 In this sub query     (select actor_id, LISTAGG(DISTINCT A.stock_symbol, ', ') WITHIN GROUP (ORDER BY A.stock_symbol) as stocks_bought
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS A 
    where 1=1
        and txn_status = 'ORDER_SUCCESS'
        and type = 'BUY'
    group by 1) T we are creating a list of distinct stocks the user has bought
 account_status = 'ACTIVE' is applied to filter in active uss account holders  first_success_add_fund_amt_usd >= 15 and AUM_USD < 5 is the filter for churn
 LISTAGG(DISTINCT A.stock_symbol, ', ') WITHIN GROUP (ORDER BY A.stock_symbol) this function is used to convert different entries in a row into a list*/
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
    sql="""/* we are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. 

 date_trunc(month, B.first_success_add_fund_date) is a function used to extract month from date*/
select date_trunc(month, B.first_success_add_fund_date) as first_add_fund_month, count(distinct B.actor_id) as total_actors
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT B
where 1=1
    and B.first_success_add_fund_date >= '20240101'
group by 1;""",
)
vn.train(
    question="""I want actor ids and moengage ids of all actors who are invested in Nvidia""",
    sql="""/* this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here
 We are joining USS_TRANSACTIONS and EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B to get Moengage IDs. firehose_id in this table is actor_id in all USS tables. This table has one row per firehose_id (actor_id) 
 stock_symbol = 'NVDA' is applied to get transactions for NVDA
 coalesce(bought_QTY ,0) coalesce(sold_QTY,0) as active_qty gives us the current active quantity of us stocks*/
select  actor_id, MOENGAGE_ID
from 
(select actor_id,MOENGAGE_ID,
    sum(case when  type = 'BUY' then qty_confirmed end) as bought_QTY,
    sum(case when type = 'SELL' then qty_confirmed end) as sold_QTY,
    coalesce(bought_QTY ,0) coalesce(sold_QTY,0) as active_qty
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS O
left join 
EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS VM
on O.actor_id= VM. firehose_id
where 1=1 
 and side = 'BUY'
    and txn_status = 'ORDER_SUCCESS'
    and stock_symbol = 'NVDA'
group by 1,2)
where active_qty > 0;""",
)
vn.train(
    question="""Give me the stock ids of the following stocks 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'?
tell me about these stock symbols 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'.
are these stock ids active? 'BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM'.""",
    sql="""/* We have used used EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS. This table contains all the stock level details. one row per stock. Contains details of Stocks and ETFs both

 Its good to display internal_status, stock_type in such queries. these are good to know details of each stock*/
select Symbol, ID as stock_id  , internal_status, stock_type    
from EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS where symbol in ('BKNG','MAR','ABNB','DIS','AWAY','JETS','TRIP','MMYT','CAR','UAL','EXPE','RYAAY','TCOM')
;""",
)
vn.train(
    question="""I want to see all the Wallet transactions in the last 7 weeks. Want to see User ID, Transaction_ID, time_stamp, order_type, status, amount , vendor account id. also need some user information like lifetime total add funds, Account creation date, first add fund date, last add fund date""",
    sql="""/* we have used 
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS. this table contains all wallet orders (or transactions). This table is joined with  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. We need USS_USER_BASE_FACT to get the user level information like account creation, total Add funds in the life time.
  we have only considered ACTIVE Account holders using 
  we have only considered wallet transactions of last 7 days using the created_date_ist column
*/
select W.ACTOR_ID, W. wallet_transaction_id, W. created_at_ist,W. WALLET_ORDER_TYPE, W. status, W. amount_usd, A.vendor_account_id , A. total_wallet_funds_added_usd as LTD_Add_FUNDS, 
    A. acct_creation_date_ist as USS_Account_creation_date,
    date(A. first_success_add_fund_time) as first_add_fund_date,
    date(A. last_success_add_fund_date) as last_add_fund_date
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS W
left join 
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A
on W. actor_id = A. actor_id
where A. account_status = 'ACTIVE'
    and W. created_date_ist >= current_date()  6 ;""",
)
vn.train(
    question="""I want to see all the Stock orders in last 7 days, Need the below information Actor_id, Transaction ID, order type, Status , Transaction Date , transaction amount , quantity, Stock symbol""",
    sql="""/* we have used  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here

*/
select Actor_id, Txn_ID, Type, Txn_Status, TXN_CREATED_DATE, TXN_AMOUNT_CONFIRMED_USD, QTY_CONFIRMED, STOCK_SYMBOL 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where txn_created_date >= current_date()  6;""",
)
vn.train(
    question="""I want D0, D7, D14, D30 and D365 Activation Rate/ Add Fund rate . Activation means first wallet add funds ever""",
    sql="""/* We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table. From this table we need the account creation date and first successful add fund date
  we have only considered ACTIVE Account holders using 
  we have only considered account creations of last 90 days using the created_date_ist column
 we have calculated D7_Activation_rate using  the below formula count(distinct case when  datediff(day, acct_creation_date_ist , first_success_add_fund_date) <= 6 then A.actor_id end )/ count(distinct A.actor_id) . Here we have counted the number of actors who successfully added funds in first 7 days of account creation*/
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
    and date(acct_creation_start_time_ist) >= current_date()90

group by 1,2,3 
order by 1;""",
)
vn.train(
    question="""Give details of about wallet transaction of a customer. need     ACTOR_ID,Transaction id,time to complete transaction in minutes,
    transaction timestamp,
    amount of transaction, transaction type""",
    sql="""/* We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS. this table contains all wallet orders (or transactions)

*/
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
    sql="""/* We have EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A which is a user level table.  From this table we need account status of an actor and first success_add_funds of an actor
 We are joining USS_USER_BASE_FACT and EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B to get Moengage IDs. firehose_id in this table is actor_id in all USS tables. This table has one row per firehose_id (actor_id) 

 we have applied account_status = 'ACTIVE' filter to filter in only USS broker account holders
 we have applied  first_success_add_fund_date is null filter to filter in users who have not added any funds
*/
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
    sql="""/* we have used  EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
this table contains all USS Stock orders (or transactions). All the Stock Buy and sell transactions will be stored here
 we have applied filter on stock_symbol column to filter in listed stocks
 date filter is also applied to filter out last 7 days
*/
select txn_created_date , count(*) as txns
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS A
where type = 'BUY'
    and stock_symbol in ('NEM','IAU','GOLD','AAAU','FNV','GFI','AEM','GDX','AU')   
    and txn_created_date >= current_date()  6
group by 1
order by 1;""",
)
vn.train(
    question="""I want to see the monthly total add funds, total withdraw funds and the difference between them from January 1st 2024 onwards.""",
    sql="""/* EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY which has daily activity data of a user. This data is at an actor day level. From this table we are extracting activity month, activity date, and number of wallet add fund amount and wallet withdraw amount
we have applied filters to select the actors whose activity is from January 1st 2024 and onwards
we use date_trunc(month, created_date_ist) to extract month from date we have used sum(total_wallet_funds_added_usd) to extract the total funds added in a month, sum(total_wallet_funds_withdraw_usd) to extract total funds withdrawn in a month.*/
select date_trunc(month, created_date_ist) as mth, sum(total_wallet_funds_added_usd) as Add_funds, sum(total_wallet_funds_withdraw_usd) as WithdRAW_FUNDS, coalesce(Add_funds,0)  coalesce(WithdRAW_FUNDS,0) as total_wallet_funds_withdraw_usd from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY where 1=1 and created_date_ist >= '20240101' group by 1;""",
)
vn.train(
    question="""I want to see the daily churn count for users who had an AUM of 15 USD or greater the previous day and whose AUM fell below 15 USD on the current day, for users who added at least 15 USD total add fund transaction and who have activity starting from January 1st 2024 onwards.""",
    sql="""/* EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY which has daily activity data of a user. This data is at an actor day level. We are extracting AUM delta from this table (AUM_DELTA_USD) which gives the change in AUM on each activity day. We also extract the CREATED_DATE_IST and ACTOR_ID. These are essential for calculating cumulative AUM (using the window function) and determining daily churn. We also join it with EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT. This is a user level table to get the total_wallet_funds_added_usd which is used to filter for users who have added at least 15 USD in total.
 we have applied filters to select the actors for whom who added fund post jan 1st B. total wallert add funds amount >= 15 and for actors whose activity is from January 1st 2024 and onwards
we use sum(coalesce(AUM_DELTA_USD,0)) over(partition by A. actor_id order by CREATED_DATE_IST rows between unbounded preceding and current row ) as AUM to calculate cumulative AUM by user from the first day of their activity, we use lag(AUM) over(partition by actor_id order by created_date_ist ) as prev_day_AUM to calculate previous day AUM for the user. Finally, we use count(distinct case when prev_day_AUM >= 15 and AUM < 15 then actor_id end) as churn to identify users whose AUM has dropped below 15 from being above 15 on the previous day*/
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
and CREATED_DATE_IST >= '20240101'
))
group by 1""",
)
vn.train(
    question="""I need all distinct user ids and their associated moengage_ids of users who visited USS in last 30 days""",
    sql="""/* EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A which has user events data related to US stocks. This table has actor_id, timestamp_ist, event, and other columns related to events. We join it with EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS to get the moengage id
 we have applied filters to select the actors whose activity is from last 30 days and onwards and have visited USS. These are the events which signify US Stock visit ('USSLandingPageLoad','USSCollectionPageload','USSDetailsPageLoaded')
 we use distinct actor_id, moengage_id to extract unique actor_id and moengage_id who have performed any of the events*/
select 
    distinct actor_id, moengage_id
from EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A
left join 
 EPIFI_DATALAKE_TECH.VENDORMAPPING.DP_VENDOR_MAPPINGS B
on A. actor_id = B. firehose_id
where 1= 1
    and date(timestamp_ist) >= current_date() 30
     and date(timestamp_ist) < current_date()
    and event in ('USSLandingPageLoad','USSCollectionPageload','USSDetailsPageLoaded')""",
)
vn.train(
    question=""" I need all distinct actor_ids who have visited the ETF stock page last 6 days.
""",
    sql="""/* EPIFI_DATALAKE_ALPACA.EVENTS.USS_INVEST_SERVER_EVENTS which has server events data related to US stocks. This table has actor_id, timestamp_ist, event, and other columns related to events. We extract the stock_id from the properties column using parse_json(properties):stock_id and join it with EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS which has details of stocks and ETFs
 we have applied filters to select the actors who have visited stock page (Event for stock page visit is 'USSDetailsPageLoadedServer') and whose activity is from last 6 days and onwards. We also filter the stocks based on stock_type = 'STOCK_TYPE_ETF' to filter inly ETF page visits
 we use distinct actor_id to extract unique actor_id who have visited the Stock page of an ETF stock in the past 6 days*/
        (select Distinct Actor_id
        from
        (select actor_id, parse_json(properties):stock_id as stock_id
        from EPIFI_DATALAKE_ALPACA.EVENTS.USS_INVEST_SERVER_EVENTS
        where 1=1
            and event = 'USSDetailsPageLoadedServer'
             and parse_json(properties):stock_id
            and date( timestamp_ist) >= current_date()  6
        group by 1,2) A
        inner join
        (select id as stock_id
        From EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS
        where 1=1
            and stock_type = 'STOCK_TYPE_ETF') B
        on A. stock_id  = B. stock_id)""",
)
vn.train(
    question="""What is the average amount of successful "Add Funds" wallet transactions in the past 30 days? / What is the average add fund amount in last 30 days""",
    sql="""/* EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS which contains all the wallet transactions data. We are extracting the amount_usd from this table
 we have applied filters to select the actors whose wallet_order_type_derived is 'Add Funds'  to filter Add fund transactions only and status is 'WALLET_ORDER_STATUS_SUCCESS' to filter success transctions only and whose activity is from last 30 days and onwards
 we use avg(amount_usd) to calculate the average add funds amount in the past 30 days*/
select avg(amount_usd)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS
where wallet_order_type_derived = 'Add Funds'
and status = 'WALLET_ORDER_STATUS_SUCCESS'
and created_date_ist >= current_date() 30;""",
)
vn.train(
    question="""What is the minimum amount of the first successful add funds transaction for users who added funds on the same day they created their accounts?""",
    sql="""/* EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT which is a user level table. From this table we extract the first_success_add_fund_amt_usd column
 we have applied filters to select the actors whose account creation date is the same as their first successful add funds date
 we use min(first_success_add_fund_amt_usd) to calculate the minimum first successful add funds amount for users who added funds on the same day they created their accounts.*/
select min(first_success_add_fund_amt_usd)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where acct_creation_date_ist = first_success_add_fund_date
and 1=1;""",
)
vn.train(
    question="""I want daywise USS account creation starters. """,
    sql="""/* EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A which has user events data related to US stocks. This table has actor_id, timestamp_ist, event, and other columns related to events.
 we have applied filters to select the actors whose event is in the list of events mentioned in the events column which are valid for account creation starters and whose activity is from Feb 1st 2024 and till yesterday's date
 we use date(timestamp_ist) as DATE1 to extract the date from timestamp_ist and count(distinct actor_id) as ACTORS to count the distinct actor ids who performed the event
Events of Account creation starters are 
('USSSetUpAccountBottomSheetload',
                'USSCreateProfileScreenLoaded',
                'USSCollectRiskLevelScreenLoaded',
                'USSDocumentsSubmissionInfoScreenload',
                'USSDisclaimerDetailsPageload',
                'USSPANUploadScreenload',
                'USSPANValidationTerminalScreenload',
                'USSSourceOfFundsScreenload',
                'USSEmployerDetailsScreenload'). If any of the above events fire for a user we can consider the user as an account creation starter*/
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
    and date(timestamp_ist) >= '20240201'
    and date(timestamp_ist) <= current_date()1
group by 1
order by 1; """,
)
vn.train(
    question="""I want to see the daily count of account creations feb 1st onwards""",
    sql="""/* EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT which is a user level table. We are extracting the acct_creation_date_ist and actor_id from this table
 we have applied filters to select the actors whose account status is 'ACTIVE' and whose account creation date is from Feb 1st 2024 and till yesterday's date
 we use acct_creation_date_ist to extract the account creation date and count(distinct actor_id) to count the number of distinct actors who created their accounts on that date*/
select acct_creation_date_ist, count(distinct actor_id)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where ACCOUNT_STATUS = 'ACTIVE'
    and acct_creation_date_ist >= '20240201'
    and acct_creation_date_ist <= current_date()1
group by 1;    """,
)
vn.train(
    question="""I want to see day wise Activations in last 30 days / I want to see the daily count of distinct actors who have performed their first successful "Add Funds" wallet transaction in the past 30 days.""",
    sql="""/* EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS W which contains all the wallet transactions data. We are extracting the created_date_ist and actor_id from this table. We also extract NEW_REPEAT_ADDFUND_USS 
 we have applied filters to select the actors whose wallet_order_type_derived is 'Add Funds' and whose NEW_REPEAT_ADDFUND_USS is 'New' to filter in only first time add fund actors. activations new actors adding funds. mean and status is 'WALLET_ORDER_STATUS_SUCCESS' and whose activity is from last 30 days and onwards
 we use created_date_ist to extract the date and count(distinct actor_id) as activations to count the number of distinct actors who have performed their first successful add funds transaction in the past 30 days.*/
select created_date_ist, count(distinct actor_id) as activations
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS W
where 1=1
    and wallet_order_type_derived = 'Add Funds'
    and NEW_REPEAT_ADDFUND_USS = 'New'
    and status = 'WALLET_ORDER_STATUS_SUCCESS'
    and created_date_ist >= current_date() 30
    ;""",
)
vn.train(
    question="""I want to see day wise Add fund starters starting Feb 1st 2024 """,
    sql="""/* EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS which has user events data related to US stocks. This table has actor_id, timestamp_ist, event, and other columns related to events.
 we have applied filters to select the actors who started add fund (events for add fund starters are 'USSBuyButtonClick', 'USSAddFundsToWalletInputAmountPageLoad') mentioned in the event column and whose activity is from Feb 1st 2024 and till yesterday's date. any of the above events fire for a user we can consider the user as an wallet add fund creation starter
 we use actor_id, date(timestamp_ist) as created_date to extract the date from timestamp_ist and */
select created_date, count(distinct actor_id) as actors
from 
    ( select  actor_id ,date(timestamp_ist) as created_date
    from EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS
    where 1=1
    and event in 
        (
        'USSBuyButtonClick',
        'USSAddFundsToWalletInputAmountPageLoad'
        )
    and date(timestamp_ist) >= '20240201'
    and date(timestamp_ist) < current_date()
    group by 1,2)
group by 1;""",
)
vn.train(
    question="""For active US Stock accounts created between 7 and 30 days ago, what is the time it took for each user to make their first successful fund addition (in seconds, minutes, and hours) after account creation?""",
    sql="""/* We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT. This is a userlevel table with information about US Stock accounts, including the actor_id, acct_creation_time_ist, and first_success_add_fund_time columns that we are extracting.
 We are only considering accounts with status 'ACTIVE' indicating they are successfully created.  We are filtering accounts created between 7 and 30 days ago (excluding today) using date(acct_creation_time_ist) between current_date() 30 and current_date()  7.  We are making sure the user has added funds (first_success_add_fund_time is not null).
 We are selecting the actor_id (user identifier).  We are calculating the time it took for the user to add funds (activate their account) using the datediff function in seconds, minutes, and hours.*/
select actor_id ,
    datediff(second,acct_creation_time_ist, first_success_add_fund_time ) as time_to_activate_sec,
    datediff(minute,acct_creation_time_ist,first_success_add_fund_time ) as time_to_activate_min,
    datediff(hour,acct_creation_time_ist,first_success_add_fund_time ) as time_to_activate_hour
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where 1=1
    and account_status = 'ACTIVE'
    and date(acct_creation_time_ist) between current_date() 30 and current_date()  7 
    and first_success_add_fund_time is not null;""",
)
vn.train(
    question="""For the past 30 days (excluding today), how many users visited the stock details page for the stocks 'GOOGL', 'AAPL', 'MSFT', 'TSLA', and 'AMZN' each day?/ Give me the daily trend of how many users visited GOOGL', 'AAPL', 'MSFT', 'TSLA', and 'AMZN' in the last 30 days""",
    sql="""/* We are using EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS (aliased as 'A'). This table stores all the events that happen on the US Stocks app or website. It includes the timestamp_ist and properties columns.  We are also using EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS (aliased as 'B'). This table contains information about stocks, including the id and symbol columns.
 We are filtering events where the event is 'USSDetailsPageLoaded' which is the event for stock details page visit, indicating the user visited a stock details page.  We are also filtering stocks where the symbol is in the list ('GOOGL','AAPL','MSFT','TSLA','AMZN').  We are selecting events that occurred between 1 and 30 days ago (excluding today) using date(timestamp_ist) >= current_date() 30 and date(timestamp_ist) <= current_date()  1.
 We are extracting the date(timestamp_ist) as date1.  We are counting the count(distinct actor_id) as users to get the number of distinct users who visited the details page of these specific stocks.*/
    select date(timestamp_ist) as date1, 
        count(distinct actor_id) as users        
    from EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A
    left join
    EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS B
        on parse_json(A. properties):stock_id ::string = B.id
    where 1=1
    and event  in (
                'USSDetailsPageLoaded'  Event for Stock Visits
                )
    and B. symbol in ('GOOGL','AAPL','MSFT','TSLA','AMZN')                
    and date(timestamp_ist) >= current_date() 30 
    and date(timestamp_ist) <= current_date()  1
    group by 1""",
)
vn.train(
    question="""Give me the daily add fund failure amount split by failure reasons . only consider activity of users who had experienced failure and werent able to do a single successful transaction""",
    sql="""/* We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY (aliased as 'A'). This is a dailylevel table with information about US Stock accounts, including created_date_ist, failure_reason_add_fund, failed_add_fund_amount_usd, and success_add_fund_amount_usd columns.
 We are filtering data for the past 7 days (excluding today) using created_date_ist >= current_date()7 and created_date_ist < current_date().  We are only considering entries where the failed_add_fund_amount_usd is greater than 0.  We are also checking if the success_add_fund_amount_usd is either 0 or null to make sure that we're only counting failed attempts and not successful ones.
 We are extracting created_date_ist (date of the event) and failure_reason_add_fund (the reason for the failed add fund attempt).  We are summing sum(failed_add_fund_amount_usd) as failed_dollar_amount to calculate the total amount of failed add fund attempts in USD.*/
select created_date_ist,failure_reason_add_fund, sum(failed_add_fund_amount_usd) as failed_dollar_amount
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY A
where 1=1 
    and created_date_ist >= current_date()7
    and created_date_ist < current_date()
    and failed_add_fund_amount_usd > 0 
    and (success_add_fund_amount_usd = 0 or success_add_fund_amount_usd is null)
group by 1,2;""",
)
vn.train(
    question="""Day wise Add fund starter to end conversion for the last 30 days. Conversion should happen in the same day as add fund start. End event is the user successfully adding funds""",
    sql="""/* We are using EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A which is an event table. From this table we are extracting date and actor_id
 Its joined with EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS. This is a wallet transaction level table. to get first add fund date. We are considering only add funds transactions which are successful.
 we have applied filters to select the actors for whom whostarted adding funds ( events for add fund starters   'USSAddFundsToWalletInputAmountPageLoad') 30 days
 we have applied filters to select the actors for whom who successfully added funds in the last 90 days.
*/
select A.created_date_ist,  count(distinct B. actor_id)/ count(distinct A. actor_id) add_fund_start_to_end_conversion
from 
( select  actor_id ,date(timestamp_ist) as created_date_ist, 
from EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A
where 1=1
and event in 
    (
    'USSAddFundsToWalletInputAmountPageLoad'
    )
and date(timestamp_ist) >= current_date()  30
and date(timestamp_ist) < current_date()
group by 1,2) A
left join 
(select actor_id, created_date_ist
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS
where 1=1
    and wallet_order_type_derived = 'Add Funds'
    and status = 'WALLET_ORDER_STATUS_SUCCESS'
    and created_date_ist >= current_date() 30
group by 1,2    ) B
on A.actor_id = B.actor_id 
and A.created_date_ist = B.created_date_ist
group by 1
order by 1; """,
)
vn.train(
    question="""Day wise Account Creation starter to end conversion for the last 30 days. Conversion should happen in the same day as account creation start. End event is the user successfully adding funds""",
    sql="""/*" We are using EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A which is an event table. From this table we are extracting date and actor_id
 Its joined with EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT UBF. This is a user level table. to get account creation date. We are only considering active accounts. "
" we have applied filters to select the actors for whom the following events were fired 'USSSetUpAccountBottomSheetload', 'USSCreateProfileScreenLoaded', 'USSCollectRiskLevelScreenLoaded', 'USSDocumentsSubmissionInfoScreenload', 'USSDisclaimerDetailsPageload', 'USSPANUploadScreenload', 'USSPANValidationTerminalScreenload', 'USSSourceOfFundsScreenload', 'USSEmployerDetailsScreenload". If any of the above events are fired we can consider them as account creation starters
 we use date(timestamp_ist) to extract date from timestamp */
select A.created_date_ist,  count(distinct B. actor_id)/ count(distinct A. actor_id) Account_creation_start_to_end_conversion
from 
( 
select  actor_id ,date(timestamp_ist) as created_date_ist, 
from EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS A
where 1=1
and event in 
    (
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
and date(timestamp_ist) >= current_date()  30
and date(timestamp_ist) < current_date()
group by 1,2) A
left join 
    (select actor_id, acct_creation_date_ist as created_date_ist
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT UBF
    where 1=1
        and account_status = 'ACTIVE'
        and acct_creation_date_ist >= current_date() 30
    group by 1,2    ) B
on A.actor_id = B.actor_id 
and A.created_date_ist = B.created_date_ist
group by 1
order by 1; """,
)
vn.train(
    question=""" How is the wallet addfund success Rate Trending in the last 7 days. Give me user and transaction level success rates""",
    sql="""/*" We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY which has daily activity data of a user. This data is at an actor day level". This has data of number of success add fund transactions , number of failed wallet transactions etc at a user day level
 we have applied filters to select the actors for whom who did activity in last 7 days. We did this because we want to see last 7 day trend
 We have used     sum(num_wallet_add_fund_success_txns)*1.00/nullif(sum(num_wallet_add_fund_txns),0) as       
    Add_fund_txn_success_rates,
    count(distinct case when success_add_fund_amount_usd > 0 then actor_id end ) / nullif(count(distinct case when num_wallet_add_fund_txns >0 then actor_id end),0) as Add_fund_user_success_rates to calculate success rates at transaction level and user level*/
select created_date_ist,
    sum(num_wallet_add_fund_success_txns)*1.00/nullif(sum(num_wallet_add_fund_txns),0) as       
    Add_fund_txn_success_rates,
    count(distinct case when success_add_fund_amount_usd > 0 then actor_id end ) / nullif(count(distinct case when num_wallet_add_fund_txns >0 then actor_id end),0) as Add_fund_user_success_rates
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY
where 1=1
    and created_date_ist >= current_date()  6
group by 1
order by 1""",
)
vn.train(
    question="""How is the wallet success Rate Trending in the last 7 days. Give me user and transaction level success rates""",
    sql="""/*" We are using EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY which has daily activity data of a user. This data is at an actor day level". This has data of number of success add fund transactions , number of failed wallet transactions etc at a user day level
 we have applied filters to select the actors for whom who did activity in last 7 days. We did this because we want to see last 7 day trend
    sum(coalesce(num_wallet_add_fund_success_txns,0) + coalesce(num_wallet_withdraw_fund_success_txns,0))*1.00/nullif(sum(num_wallet_txns),0) as       
    _txn_success_rates,
    count(distinct case when (coalesce(num_wallet_add_fund_success_txns,0) + coalesce(num_wallet_withdraw_fund_success_txns,0)) > 0 then actor_id end ) / nullif(count(distinct case when num_wallet_txns >0 then actor_id end),0) as Wallet_user_success_rates to calculate success rates at transaction level and user level*/
select created_date_ist,
    sum(coalesce(num_wallet_add_fund_success_txns,0) + coalesce(num_wallet_withdraw_fund_success_txns,0))*1.00/nullif(sum(num_wallet_txns),0) as       
    _txn_success_rates,
    count(distinct case when (coalesce(num_wallet_add_fund_success_txns,0) + coalesce(num_wallet_withdraw_fund_success_txns,0)) > 0 then actor_id end ) / nullif(count(distinct case when num_wallet_txns >0 then actor_id end),0) as Wallet_user_success_rates
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY
where 1=1
    and created_date_ist >= current_date()  6
group by 1
order by 1""",
)
vn.train(
    question="""How many users have NVDA in their watchlist?""",
    sql="""/*" We are using EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS WSM which is a watchlist stock mapping table. This table maps the watchlist with the stock symbol.
 Its joined with EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS W. This is a watchlist table which maps all the watchlists to the actor_id . Its also joined with EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS. This table contains all the stock level details. one row per stock. Contains details of Stocks and ETFs both. " Stock table is joined with watchlist stock mappings. We are extracting symbol name from the 
" we have applied filter on s. symbol = 'NVDA' to filter out all the users who have watchlisted NVDA"
we are selecting actor_ids*/
select distinct W.actor_id
from EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLIST_STOCK_MAPPINGS WSM
left join 
EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.WATCHLISTS W
on WSM. watchlist_id = W. id
left join 
EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS S
on WSM.stock_id = S.id
where 1=1
    and s. symbol = 'NVDA';""",
)
vn.train(
    question="""Give me the daily trend of USS AUM of last 60 days""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY: Daily user activity data, including CREATED_DATE_IST and AUM_DELTA_USD. Columns used: CREATED_DATE_IST, AUM_DELTA_USD.
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT: User-level information, including ACTOR_ID and total_wallet_funds_added_usd. Column used: ACTOR_ID.
CREATED_DATE_IST >= '2023-11-01' (in USS_USER_DAILY): Filters for users who have activity starting from November 1st, 2023.
total_wallet_funds_added_usd > 0  (in USS_USER_BASE_FACT): Filters for users who have added funds to their US Stock account.
date1: Extracts the date of the order.
SUM(AUM) AS AUM: Calculates the sum of the cumulative AUM for each date, considering all users who have added funds.

Approach:
1. Create a CTE (`dm`) to map order dates to investment months for all users with a successful "Add Funds" transaction.
2. Create another CTE (`USS_user_aum`) to calculate the cumulative AUM for each user based on order date and investment month.
3.  Group the results by order date and calculate the total AUM for each date. 
*/
With dm as 
(
select ACTOR_ID, date1, inv_month
    from    (
            select CREATED_DATE_IST as date1, date_trunc(month, CREATED_DATE_IST) as inv_month
            from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY
            where CREATED_DATE_IST >='2023-11-01'
            group by 1,2
    ) a
cross join 
    (
    select actor_id
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
    where 1=1
    and total_wallet_funds_added_usd > 0
    ) b
group by 1,2,3
),
USS_user_aum as (
select d.ACTOR_ID, d.date1,d.inv_month as aum_month,
sum(coalesce(AUM,0)) over(partition by d.actor_id order by d.date1 rows between unbounded preceding and current row) as aum
from dm d
left join
(
select CREATED_DATE_IST as mth,
actor_id, sum(aum_delta_USD) as aum
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY
group by 1,2
) a
on d.actor_id = a.actor_id and d.date1 = a.mth
)
select *
from 
(select date1 , sum(AUM) as AUM
from USS_user_aum
where 1=1
group by 1)
where  date1 >= current_date() - 59
""",
)
vn.train(
    question="""can you tell me what are the stocks which are in collection ID - COLLECTION_NAME_TOP_TRADED_AMONG_LEADING_MARKET_CAP? Also give me buy rating for these stocks""",
    sql="""/*
EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS: Maps stocks to specific collections. Columns used: stock_id, collection_id.
EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS: Contains detailed information about stocks, including symbol and estimates_info (which is a JSON object containing analyst ratings). Columns used: symbol, estimates_info.
csm.collection_id = 'COLLECTION_NAME_TOP_TRADED_AMONG_LEADING_MARKET_CAP': Filters for stocks belonging to the collection with the ID 'COLLECTION_NAME_TOP_TRADED_AMONG_LEADING_MARKET_CAP'. 
s.symbol: Extracts the stock symbol.
coalesce((parse_json(s. estimates_info):analystRecommendations:buy ::numeric),0)*1.00 / nullif((coalesce((parse_json(s. estimates_info):analystRecommendations:buy ::numeric),0) + coalesce((parse_json(s. estimates_info):analystRecommendations:hold ::numeric),0) + coalesce((parse_json(s. estimates_info):analystRecommendations:sell ::numeric),0)),0) as buy_rating: Calculates the percentage of "Buy" ratings by analysts for each stock in the specified collection. 

Approach:
1. Join the `COLLECTION_STOCK_MAPPINGS` table with the `STOCKS` table using the `stock_id` column.
2. Filter for stocks that belong to the collection with ID `'COLLECTION_NAME_TOP_TRADED_AMONG_LEADING_MARKET_CAP'`.
3.  Parse the `estimates_info` JSON field to extract the "Buy", "Hold", and "Sell" ratings.
4.  Calculate the percentage of "Buy" ratings for each stock. Buy rating is the percentage of analysts who have rated the stock as a buy
*/
SELECT 
    s.symbol, coalesce((parse_json(s. estimates_info):analystRecommendations:buy ::numeric),0)*1.00 / 
nullif((coalesce((parse_json(s. estimates_info):analystRecommendations:buy ::numeric),0) + coalesce((parse_json(s. estimates_info):analystRecommendations:hold ::numeric),0) + 
coalesce((parse_json(s. estimates_info):analystRecommendations:sell ::numeric),0)),0) as buy_rating
FROM EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.COLLECTION_STOCK_MAPPINGS csm
JOIN EPIFI_DATALAKE_ALPACA.USSTOCKS_ALPACA.STOCKS s ON csm.stock_id = s.id
WHERE csm.collection_id = 'COLLECTION_NAME_TOP_TRADED_AMONG_LEADING_MARKET_CAP';""",
)
vn.train(
    question="""Give me the daily trend of USS AUM of last 60 days""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY: Daily user activity data, including CREATED_DATE_IST and AUM_DELTA_USD. Columns used: CREATED_DATE_IST, AUM_DELTA_USD.
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT: User-level information, including ACTOR_ID and total_wallet_funds_added_usd. Column used: ACTOR_ID.
CREATED_DATE_IST >= '2023-11-01' (in USS_USER_DAILY): Filters for users who have activity starting from November 1st, 2023.
total_wallet_funds_added_usd > 0  (in USS_USER_BASE_FACT): Filters for users who have added funds to their US Stock account.
date1: Extracts the date of the order.
SUM(AUM) AS AUM: Calculates the sum of the cumulative AUM for each date, considering all users who have added funds.

Approach:
1. Create a CTE (`dm`) to map order dates to investment months for all users with a successful "Add Funds" transaction.
2. Create another CTE (`USS_user_aum`) to calculate the cumulative AUM for each user based on order date and investment month.
3.  Group the results by order date and calculate the total AUM for each date. 
4. Then we calculated month wise AUM which is the AUM on the last day of each month. For current month we take the AUM on yesterday
*/
With dm as 
(
select ACTOR_ID, date1, inv_month
    from    (
            select CREATED_DATE_IST as date1, date_trunc(month, CREATED_DATE_IST) as inv_month
            from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY
            where CREATED_DATE_IST >='2023-11-01'
            group by 1,2
    ) a
cross join 
    (
    select actor_id
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
    where 1=1
    and total_wallet_funds_added_usd > 0
    ) b
group by 1,2,3
),
USS_user_aum as (
select d.ACTOR_ID, d.date1,d.inv_month as aum_month,
sum(coalesce(AUM,0)) over(partition by d.actor_id order by d.date1 rows between unbounded preceding and current row) as aum
from dm d
left join
(
select CREATED_DATE_IST as mth,
actor_id, sum(aum_delta_USD) as aum
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_DAILY
group by 1,2
) a
on d.actor_id = a.actor_id and d.date1 = a.mth
)

select date_trunc(month, date1) as month, AUM
from 
(select date1 , sum(AUM) as AUM
from USS_user_aum
where 1=1
group by 1)
where  date1 >= current_date() - 59
    and date1 = case when current_date()-1 < last_day(date1) then current_date()-1 else last_day(date1) end
;""",
)
vn.train(
    question="""Total stocks bought prev month versus this month / Total stocks bought prev month vs this month""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: txn_created_month, qty_confirmed, type, txn_status.
type = 'BUY': Filters for transactions where the order type is a "BUY" order.
txn_status = 'ORDER_SUCCESS': Filters for transactions where the order was successfully completed.
sum(case when txn_created_month = date_trunc(month, dateadd(month, -1, current_date())) then qty_confirmed end) as prev_month_qty: Calculates the sum of the confirmed quantities (qty_confirmed) for successful "BUY" orders that occurred in the previous month.
sum(case when txn_created_month = date_trunc(month, current_date()) then qty_confirmed end) as curr_month_qty: Calculates the sum of the confirmed quantities (qty_confirmed) for successful "BUY" orders that occurred in the current month.

Approach:
1. Filter the `USS_TRANSACTIONS` table to include only successful "BUY" orders.
2. Calculate the sum of `qty_confirmed` for orders in the previous month using `date_trunc(month, dateadd(month, -1, current_date()))`.
3. Calculate the sum of `qty_confirmed` for orders in the current month using `date_trunc(month, current_date())`.
*/
select
    sum(case when txn_created_month = date_trunc(month, dateadd(month, -1, current_date())) then qty_confirmed end) as prev_month_qty,
    sum(case when txn_created_month = date_trunc(month, current_date()) then qty_confirmed end) as curr_month_qty
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where 1=1
    and type = 'BUY' 
    and txn_status = 'ORDER_SUCCESS';""",
)
vn.train(
    question="""how many users are currently holding any stock? / how many users are currently invested in us stock?""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: actor_id, type, qty_confirmed.
net_qty > 0 (in the subquery):  Filters for users who have a positive net quantity of stocks, indicating they have bought more stocks than they have sold. this means they are holding stock and are currently invested in US Stock
count(distinct actor_id) as users_holding_stocks:  Calculates the count of unique users (actor_id) who have a positive net quantity of stocks, signifying they are currently holding stocks.

Approach:
1. Create a subquery to calculate the net quantity of stocks for each user by summing `qty_confirmed` for "BUY" orders and subtracting the sum of `qty_confirmed` for "SELL" orders.
2. Filter the subquery results to include only users with a positive `net_qty`.
3. Count the distinct users (actor_id) to determine the number of users currently holding stocks.
4. Holding a Stock means they have >0 net stocks 
*/
select count(distinct actor_id) as users_holding_stocks from ( select actor_id, sum(case when type = 'BUY' then qty_confirmed else 0 end) - sum(case when type = 'SELL' then qty_confirmed else 0 end) as net_qty from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS where txn_status = 'ORDER_SUCCESS' group by 1 ) temp where net_qty > 0;""",
)
vn.train(
    question="""How many users are holding Google? How many users are invested in Google?""",
    sql="""select count(distinct actor_id) as users_holding_stocks from ( select actor_id, sum(case when type = 'BUY' then qty_confirmed else 0 end) - sum(case when type = 'SELL' then qty_confirmed else 0 end) as net_qty from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS 
where txn_status = 'ORDER_SUCCESS' 
and STock_symbol = 'GOOGL'
group by 1 ) temp 
where net_qty > 0
    
;   """,
)
vn.train(
    question="""how many users added funds in May""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS: This table contains comprehensive information about "Add Funds" and "Withdraw Funds" transactions related to US Stocks USD wallets. Columns used: actor_id, wallet_order_type_derived, status, created_month_ist.
wallet_order_type_derived = 'Add Funds':  Filters for transactions that are "Add Funds" transactions.
status = 'WALLET_ORDER_STATUS_SUCCESS': Filters for transactions that were successful.
created_month_ist = '2024-05-01': Filters for transactions that occurred in May 2024.
count(distinct actor_id): Calculates the count of unique users (actor_id) who made successful "Add Funds" transactions in May 2024.

Approach:
1. Filter the `USS_WALLET_ORDERS` table to include only successful "Add Funds" transactions that occurred in May 2024.
2. Count the distinct users (actor_id) to determine the number of unique users who made these transactions.
*/
select count(distinct actor_id)
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS
where wallet_order_type_derived = 'Add Funds' 
and status = 'WALLET_ORDER_STATUS_SUCCESS'
and created_month_ist = '2024-05-01';""",
)
vn.train(
    question="""How many users bought crowdrstrike stocks in last 7 days?""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS:  This table contains information about US Stock transactions. Columns used: actor_id, txn_status, type, stock_symbol, txn_created_date.
txn_status = 'ORDER_SUCCESS':  Filters for transactions that were successfully completed.
type = 'BUY': Filters for transactions where the order type is a "BUY" order.
stock_symbol = 'CRWD': Filters for transactions involving the stock symbol "CRWD".
txn_created_date >= current_date() - 7: Filters for transactions that occurred in the last 7 days (including today).
count(distinct actor_id) as users_bought_crwd:  Calculates the count of unique users (actor_id) who have successfully purchased the stock "CRWD" in the last 7 days.

Approach:
1. Filter the `USS_TRANSACTIONS` table to include only successful "BUY" orders for the stock 'CRWD' within the last 7 days.
2. Count the distinct users (actor_id) to determine the number of unique users who bought 'CRWD' during that period.
*/
select count(distinct actor_id) as users_bought_crwd
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where txn_status = 'ORDER_SUCCESS'
  and type = 'BUY'
  and stock_symbol = 'CRWD'
  and txn_created_date >= current_date() - 7;""",
)
vn.train(
    question="""what is the median value of buy order amount in the last 30 days""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: txn_amount_confirmed_usd, txn_created_date, type, txn_status.
txn_created_date >= dateadd(day, -30, current_date()): Filters for transactions that occurred in the last 30 days (including today).
type = 'BUY': Filters for transactions where the order type is a "BUY" order.
txn_status = 'ORDER_SUCCESS': Filters for transactions where the order was successfully completed.
median(txn_amount_confirmed_usd) as median_successful_buy_order_value:  Calculates the median value of the confirmed transaction amount in USD (txn_amount_confirmed_usd) for successful "BUY" orders within the last 30 days.

Approach:
1. Filter the `USS_TRANSACTIONS` table to include only successful "BUY" orders within the last 30 days.
2. Calculate the median value of the confirmed transaction amounts (`txn_amount_confirmed_usd`) for those orders.
*/
select median(txn_amount_confirmed_usd) as median_successful_buy_order_value
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where txn_created_date >= dateadd(day, -30, current_date())
  and type = 'BUY'
  and txn_status = 'ORDER_SUCCESS';""",
)
vn.train(
    question="""what is the 25th, 75th, 90th percentile of Buy transaction amount""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: txn_amount_confirmed_usd, txn_created_date, type, txn_status.
txn_created_date >= dateadd(day, -6, current_date()): Filters for transactions that occurred in the last 6 days (including today).
type = 'BUY': Filters for transactions where the order type is a "BUY" order.
txn_status = 'ORDER_SUCCESS': Filters for transactions where the order was successfully completed.
approx_percentile(txn_amount_confirmed_usd, 0.25)  as P25: Calculates the approximate 25th percentile of the confirmed transaction amounts in USD (txn_amount_confirmed_usd) for successful "BUY" orders within the last 6 days.
approx_percentile(txn_amount_confirmed_usd, 0.75)  as P75: Calculates the approximate 75th percentile of the confirmed transaction amounts in USD (txn_amount_confirmed_usd) for successful "BUY" orders within the last 6 days.
approx_percentile(txn_amount_confirmed_usd, 0.90)  as P90: Calculates the approximate 90th percentile of the confirmed transaction amounts in USD (txn_amount_confirmed_usd) for successful "BUY" orders within the last 6 days.

Approach:
1. Filter the `USS_TRANSACTIONS` table to include only successful "BUY" orders within the last 6 days.
2. Calculate the approximate 25th, 75th, and 90th percentiles of the confirmed transaction amounts (`txn_amount_confirmed_usd`) for those orders using the `approx_percentile` function.
*/
select approx_percentile(txn_amount_confirmed_usd, 0.25)  as P25,
        approx_percentile(txn_amount_confirmed_usd, 0.75)  as P75,
        approx_percentile(txn_amount_confirmed_usd, 0.90)  as P90
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS
where txn_created_date >= dateadd(day, -6, current_date())
  and type = 'BUY'
  and txn_status = 'ORDER_SUCCESS';""",
)
vn.train(
    question="""can you list all the columns and their descriptions in EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS W """,
    sql="""describe table EPIFI_DATAMART_ALPACA.USSTOCKS.USS_WALLET_ORDERS;""",
)
vn.train(
    question="""what % of people who have >0 AUM us stocks currently and hold at least 2 different stocks? """,
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT: User-level information, including ACTOR_ID and AUM_USD. Columns used: ACTOR_ID, AUM_USD.
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: actor_id, type, qty_confirmed, stock_id, txn_status.
None (but there are HAVING clauses within subqueries).
count(distinct B. actor_id) * 1.00 / count(distinct case when AUM_USD > 0 then A.Actor_id end) as perc_: 
    Calculates the percentage of users who are holding at least 2 different stocks (based on the B subquery) among those with a positive AUM (AUM_USD > 0).

Approach:
1. Create a subquery to calculate the net quantity of stocks for each user by summing qty_confirmed for "BUY" orders and subtracting the sum of qty_confirmed for "SELL" orders.
2. Filter the subquery results to include only users with a positive net_qty.
3. Create another subquery to count the number of distinct stocks held by each user and filter users who are holding more than 1 stocks
4. Join the user-level information (USS_USER_BASE_FACT) with the subquery results to identify users holding at least 2 stocks.
5. Calculate the percentage of these users among those with a positive AUM.
*/
select  
    count(distinct B. actor_id) * 1.00 / count(distinct case when AUM_USD > 0 then A.Actor_id end) as perc_
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT A
left join 
    (select actor_id, count(distinct stock_id) as num_stocks_holding
    from 
    (select actor_id, stock_id,
        sum(case when type = 'BUY' then qty_confirmed else 0 end) - sum(case when type = 'SELL' then qty_confirmed else 0 end) as net_qty 
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS T
    where txn_status = 'ORDER_SUCCESS' 
    group by 1,2  
    having net_qty > 0)
    group by 1
    having num_stocks_holding >= 2) B
on A. actor_id = B. actor_id""",
)
vn.train(
    question="""print the stocks of the user who currently holds the most stocks?""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: actor_id, type, qty_confirmed, stock_symbol, stock_id, txn_status.
None (but there are HAVING clauses within subqueries).
stock_symbol: Extracts the stock symbol from the A subquery.

Approach:
1.  Calculate the net quantity of stocks for each user by summing `qty_confirmed` for "BUY" orders and subtracting the sum of `qty_confirmed` for "SELL" orders. Filter for users with a positive net quantity.
2.  Count the number of distinct stocks held by each user, ranking them based on the count in descending order.
3.  Select the user with the highest number of distinct stocks (the user with rank = 1).
4.  Finally, join the results with the table that has the net quantities for users to identify the stock symbol held by that user.
*/
select  stock_symbol
from 
(select actor_id,stock_symbol,
    sum(case when type = 'BUY' then qty_confirmed else 0 end) - sum(case when type = 'SELL' then qty_confirmed else 0 end) as net_qty 
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS T
where txn_status = 'ORDER_SUCCESS' 
group by 1,2 
having net_qty > 0) A
inner join     
(select 
actor_id, 
    count(distinct stock_id) as num_stocks_holding, 
    row_number() over( order by num_stocks_holding desc ) rnk
from 
    (select actor_id, stock_id,
        sum(case when type = 'BUY' then qty_confirmed else 0 end) - sum(case when type = 'SELL' then qty_confirmed else 0 end) as net_qty 
    from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS T
    where txn_status = 'ORDER_SUCCESS' 
    group by 1,2  
    having net_qty > 0)
group by 1
qualify rnk = 1
)B
on A. actor_id = B. actor_id
;""",
)
vn.train(
    question="""What is the average and median time (in days) to purchase first US stock post account creation?""",
    sql="""/*To calculate the average time to first purchase:
1. We filter for only active accounts where first_buy_date is not null (accounts that made a purchase)
2. We calculate the difference between first_buy_date and acct_creation_date_ist in days using datediff()
3. We take the average of this difference 

To calculate the median time:
1. We filter for only active accounts where first_buy_date is not null
2. We calculate the difference between first_buy_date and acct_creation_date_ist in days using datediff()
3. We use the approx_percentile() function to get the 50th percentile (median) value of this difference
*/

select 
    avg(datediff(day, acct_creation_date_ist, first_buy_date)) as avg_days_to_first_purchase,
    approx_percentile(datediff(day, acct_creation_date_ist, first_buy_date), 0.5) as median_days_to_first_purchase
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT
where account_status = 'ACTIVE'
and first_buy_date is not null;""",
)
vn.train(
    question="""How many users have bought 5 stocks in first 14 days of account creation""",
    sql="""/*
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT: User-level information, including ACTOR_ID, acct_creation_date_ist, and account_status. Columns used: ACTOR_ID, acct_creation_date_ist, account_status.
EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS: This table contains information about US Stock transactions. Columns used: actor_id, txn_created_date, stock_id, txn_status, type.
txn_status = 'ORDER_SUCCESS': Filters for transactions that were successfully completed.
type = 'BUY': Filters for transactions where the order type is a "BUY" order.
U. account_status = 'ACTIVE': Filters for users whose account status is 'ACTIVE'.
count(distinct actor_id):  Calculates the count of unique users (actor_id) who meet the criteria defined within the subquery. 

Approach:
1. Create a subquery to identify users who have successfully bought 5 different stocks within the first 14 days after their account creation.
2. Filter for users with an active account status.
3. Join the `USS_USER_BASE_FACT` table with the `USS_TRANSACTIONS` table to identify transactions within the specified timeframe.
4. Count the distinct users who meet the criteria to determine the number of users who have bought 5 different stocks within the first 14 days.
*/
select count(distinct actor_id) 
from 
(select U.actor_id
from EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT U
left join EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS T
on T. actor_id = U. actor_id
and T. txn_created_date <= dateadd(day, 13, acct_creation_date_ist)
where txn_status = 'ORDER_SUCCESS'
    and type = 'BUY'
    and U. account_status = 'ACTIVE'
group by 1    
having count(distinct stock_id) = 5)""",
)
vn.train(
    question="""The conversion rate of US Stocks details page is defined as the number of people who bought or sold a stock on the same day after landing on US Stocks details page. Can you tell me the conversion rate? Can you exclude users who don't have an active account when they visit the stock details page? You can refer to account creation date ist to refer to when the account became active""",
    sql="""/*
stock_visitors:  A Common Table Expression (CTE) that identifies unique users who have visited the "USSDetailsPageLoaded" page. Columns used: actor_id, visit_date.
successful_orders: A CTE that identifies unique users who have placed successful orders. Columns used: actor_id, order_date.
active_users: A CTE that identifies active users (account_status = 'ACTIVE'). Columns used: actor_id, acct_creation_date_ist.
E.event = 'USSDetailsPageLoaded' (in stock_visitors): Filters for events where the user has loaded the stock details page.
T.txn_status = 'ORDER_SUCCESS' (in successful_orders): Filters for transactions that were successfully completed.
U.account_status = 'ACTIVE' (in active_users): Filters for users whose accounts are active.
ROUND(COUNT(DISTINCT CASE WHEN O.actor_id IS NOT NULL THEN V.actor_id END) * 1.0 / COUNT(DISTINCT V.actor_id), 2) AS conversion_rate:  Calculates the conversion rate, rounded to 2 decimal places, by dividing the number of distinct users with successful orders who also visited the stock details page by the total number of distinct users who visited the stock details page. 

Approach:
1. Create CTEs to identify unique stock visitors, successful order placers, and active users.
2.  Left join `stock_visitors` with `successful_orders` to identify users who have both visited the stock details page and placed a successful order on the same day.
3. Inner join with `active_users` to include only active users and transactions occurring after account creation.
4. Calculate the conversion rate by dividing the count of distinct users with successful orders (who also visited the stock details page) by the total count of distinct stock visitors. 
*/
WITH stock_visitors AS (
  SELECT DISTINCT
    E.actor_id,
    DATE(E.timestamp_ist) AS visit_date
  FROM EPIFI_DATALAKE_TECH.EVENTS.USS_INVEST_CLIENT_EVENTS E
  WHERE E.event = 'USSDetailsPageLoaded'
),
successful_orders AS (
  SELECT DISTINCT
    T.actor_id,
    DATE(T.txn_created_date) AS order_date
  FROM EPIFI_DATAMART_ALPACA.USSTOCKS.USS_TRANSACTIONS T
  WHERE T.txn_status = 'ORDER_SUCCESS'
),
active_users AS (
  SELECT
    U.actor_id,
    U.acct_creation_date_ist
  FROM EPIFI_DATAMART_ALPACA.USSTOCKS.USS_USER_BASE_FACT U
  WHERE U.account_status = 'ACTIVE'
)
SELECT
  ROUND(
    COUNT(DISTINCT CASE WHEN O.actor_id IS NOT NULL THEN V.actor_id END) * 1.0
    / COUNT(DISTINCT V.actor_id),
    2
  ) AS conversion_rate
FROM stock_visitors V
LEFT JOIN successful_orders O
  ON V.actor_id = O.actor_id
  AND V.visit_date = O.order_date
INNER JOIN active_users A
  ON V.actor_id = A.actor_id
  AND V.visit_date >= DATE(A.acct_creation_date_ist);""",
)
