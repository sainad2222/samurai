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
    documentation="""Top of funnel

Users first come to the product through any of the entrypoints. There are one of three pages where the user can land:
US Stocks landing page: 
This is the main landing page of US Stocks. This contains the explore page, and user can start their account creation or exploration journey from here.
The event to track here is ‘USSLandingPageLoad’
User can also access the watchlist page of the US stocks from the landing page. 
The event to track here is ‘USSWatchlistload’
US Stocks Details page:
This is the main stock page of US Stocks
The event to track here is ‘USSDetailsPageLoaded’.
There is an event property called ‘Stock ID’ which will be the Stock ID from the US Stocks stocks table which can be matched. It will also have a symbol property and can be queried like that. 
US Stocks collections page
There is a US Stocks collections page
The event to track here is ‘USSCollectionPageload’
There is an event property called ‘CollectionID’ which will be the collection from the US Stocks collections table which can be matched. 

Top of funnel is defined as when a user visits any of the above US Stocks page.

Top of funnel for a day is defined as when a user visits any US Stocks page in a day. 
Top of funnel for a week is defined as when a user visits any US Stocks page in a week. 
Top of funnel for a month is defined as when a user visits any US Stocks page in a month. 

This means that it will be a union of the above three events across time.
"""
)
vn.train(
    documentation="""Account Creation Starter

Any of the below events is account creation starter.

'USSSetUpAccountBottomSheetload',
                'USSCreateProfileScreenLoaded',
                'USSCollectRiskLevelScreenLoaded',
                'USSDocumentsSubmissionInfoScreenload',
                'USSDisclaimerDetailsPageload',
                'USSPANUploadScreenload',
                'USSPANValidationTerminalScreenload',
                'USSSourceOfFundsScreenload',
                'USSEmployerDetailsScreenload'

Account creation starter is defined as when a user fires any of the above events in that particular time period.

Account creation starter for the day is defined as when a user fires any of the above events in that particular day.
Account creation starter for the week is defined as when a user fires any of the above events in that particular week.

Account creation starter for the month is defined as when a user fires any of the above events in that particular month.
"""
)
vn.train(
    documentation="""Account Creation Conversion

For this, refer to User base fact table in the US Stocks datamart and then use the account creation date IST column to check whether the account is created and when it is created. Whenever anyone is looking for this metric, it should check for when the account status is active.
"""
)
vn.train(
    documentation="""Add Funds starter

Any of the below events if it is fired, will be counted as an Add funds starter. 
 'USSAddFundsToWalletInputAmountPageLoad' 
Add funds starter is defined as when a user fires any of the above events in that particular time period.

Add funds starter for the day is defined as when a user fires any of the above events in that particular day.
Add funds starter for the week is defined as when a user fires any of the above events in that particular week.

Add funds starter for the month is defined as when a user fires any of the above events in that particular month.
"""
)
vn.train(
    documentation="""Add funds Conversion

Use the USS wallet orders table from US Stocks datamart to check whether the user has added any funds in the period required. Then they are considered as converted.
"""
)
vn.train(
    documentation="""Firehose ID, Actor ID & Moengage ID

Firehose ID is just actor ID in the DP vendor mappings. Moengage ID is the ID used for communications. It’s often a common use case of product managers to fetch moengage IDs of specific set of cohorts that they need to send comms to. Firehose ID & actor ID have the same values. Hence for this use-case, fetch the actor IDs & use it to join with firehose ID in DP vendor mappings and then give moengage IDs from there."""
)
