import json
import os
import time
from datetime import datetime, timedelta
from random import randint

import boto3
import pytest
from mypy_boto3_s3.service_resource import Bucket

from src.tests.config import Config

sfn = boto3.client('stepfunctions')
STEPFUNCTION_ARN: str
bucket: Bucket
conf: Config


def setup_module(module):
    global conf
    global bucket
    conf = Config()
    if conf.stage == "prod":
        raise Exception("Invalid Stage for Integration Test")
    bucket = boto3.resource('s3').Bucket(
        f"ace-partner-integration-{conf.spmid}-{conf.stage}-us-west-2")


@pytest.fixture
def opportunity_input(execution_name):
    return {
        "version": "1",
        "spmsId": conf.spmid,
        "opportunities": [
            {
                "useCase": "Business Applications",
                "targetCloseDate": "2024-06-30",
                "projectDescription": "Automation Platform development for bank. Need support in understanding customer requirements and any background on their cloud projects",
                "postalCode": "84133",
                "partnerProjectTitle": execution_name,
                "partnerPrimaryNeedFromAws": "Deal support",
                "partnerCrmUniqueIdentifier": execution_name,
                "industry": "Financial Services",
                "expectedMonthlyAwsRevenue": 100,
                "deliveryModel": "SaaS or PaaS",
                "customerWebsite": "ally.com",
                "customerCompanyName": "Ally Segall",
                "country": "United States",
                "state": "Alaska",
                "IsOppFromMarketingActivity": "No"
            }
        ]
    }

#Create with all mandatory fields + partner sales contact details
@pytest.fixture
def opportunity_input_uat2(execution_name):
    return {
        "version": "1",
        "spmsId": conf.spmid,
        "opportunities": [
            {
                "useCase": "Business Applications",
                "targetCloseDate": "2024-06-30",
                "projectDescription": "Automation Platform development for bank. Need support in understanding customer requirements and any background on their cloud projects",
                "postalCode": "84133",
                "partnerProjectTitle": execution_name,
                "partnerPrimaryNeedFromAws": "Deal support",
                "partnerCrmUniqueIdentifier": execution_name,
                "industry": "Financial Services",
                "expectedMonthlyAwsRevenue": 100.0,
                "deliveryModel": "SaaS or PaaS",
                "customerWebsite": "ally.com",
                "customerCompanyName": "Ally Segall",
                "country": "United States",
                "state": "Alaska" , 
                "IsOppFromMarketingActivity" : "No",
                "primaryContactPhone": "5555555",
                "primaryContactLastName": "PartnerSalesRepLastName",
                "primaryContactFirstName": "PartnerSalesRepFirstName",
                "primaryContactEmail": "PartnerSalesRepLastName@partner.com"
            }
        ]
    }

#Create with all mandatory fields + partner sales contact + customer contact details
@pytest.fixture
def opportunity_input_uat3(execution_name):
    return {
        "version": "1",
        "spmsId": conf.spmid,
        "opportunities": [
            {
                "useCase": "Business Applications",
                "targetCloseDate": "2024-06-30",
                "projectDescription": "Automation Platform development for bank. Need support in understanding customer requirements and any background on their cloud projects",
                "postalCode": "84133",
                "partnerProjectTitle": execution_name,
                "partnerPrimaryNeedFromAws": "Deal support",
                "partnerCrmUniqueIdentifier": execution_name,
                "industry": "Financial Services",
                "expectedMonthlyAwsRevenue": 100.0,
                "deliveryModel": "SaaS or PaaS",
                "customerWebsite": "ally.com",
                "customerCompanyName": "Ally Segall",
                "country": "United States",
                "state": "Alaska" , 
                "IsOppFromMarketingActivity" : "No",
                "primaryContactPhone": "5555555",
                "primaryContactLastName": "PartnerSalesRepLastName",
                "primaryContactFirstName": "PartnerSalesRepFirstName",
                "primaryContactEmail": "PartnerSalesRepLastName@partner.com",
                "customerTitle": "mr",
                "customerPhone": "99999999",
                "customerLastName": "customerlastname",
                "customerFirstName": "customerfirstname",
                "customerEmail": "cust@cust.com"
            }
        ]
    }

#Create with all possible fields
@pytest.fixture
def opportunity_input_uat4(execution_name):
    return {
        "version": "1",
        "spmsId": conf.spmid,
        "opportunities": [
            {
                "useCase": "Business Applications",
                "targetCloseDate": "2024-06-30",
                "projectDescription": "Automation Platform development for bank. Need support in understanding customer requirements and any background on their cloud projects",
                "postalCode": "84133",
                "partnerProjectTitle": execution_name,
                "partnerPrimaryNeedFromAws": "Deal support",
                "partnerCrmUniqueIdentifier": execution_name,
                "industry": "Financial Services",
                "expectedMonthlyAwsRevenue": 100.0,
                "deliveryModel": "SaaS or PaaS",
                "customerWebsite": "ally.com",
                "customerCompanyName": "Ally Segall",
                "country": "United States",
                "state": "Alaska" , 
                "IsOppFromMarketingActivity" : "Yes",
                "primaryContactPhone": "5555555",
                "primaryContactLastName": "PartnerSalesRepLastName",
                "primaryContactFirstName": "PartnerSalesRepFirstName",
                "primaryContactEmail": "PartnerSalesRepLastName@partner.com",
                "customerTitle": "mr",
                "customerPhone": "99999999",
                "customerLastName": "customerlastname",
                "customerFirstName": "customerfirstname",
                "customerEmail": "cust@cust.com",
                "wWPSPDMEmail": "WWPS@AMAZON.COM",
                "wWPSPDM": "WWPS",
                "subUseCase": "SAP Production",
                "streetAddress": "123asasa",
                "status": "Approved",
                "stage": "Launched",
                "publicReferenceUrl": "HTTPS://URL.COM",
                "publicReferenceTitle": "prt",
                "partnerPrimaryNeedFromAwsOther": "other",
                "partnerDeveloperManagerEmail": "pdm@amaz.com",
                "partnerDeveloperManager": "pdm",
                "partnerAcceptanceStatus": "Rejected",
                "nextStepHistory": "nxt",
                "nextStep": "nxt",
                "leadSource": "lsource",
                "lastModifiedDate": "", 
                "lastModifiedBy": "",
                "isThisForMarketplace": "No",
                "isThisAPublicReference": "No",
                "isNetNewBusinessForCompany": "No",
                "isMarketingDevelopmentFunded": "No",
                "industryOther": "other",
                "createdDate": "",
                "createdBy": "",
                "contractVehicle": "",
                "competitiveTrackingOther": "other",
                "competitiveTracking": "Oracle Cloud",
                "closedLostReason": "",
                "city": "city",
                "campaignName": "APN Immersion Days",
                "aWSStage": "Launched",
                "aWSSalesRepName": "awsrep",
                "aWSSalesRepEmail": "awsrep@amazon.com",
                "aWSPartnerSuccessManagerName": "psm",
                "aWSPartnerSuccessManagerEmail": "psm@amazon.com",
                "aWSISVSuccessManagerName": "isvsuccessname",
                "aWSISVSuccessManagerEmail": "isv@amazon.com",
                "awsFieldEngagement": "No",
                "aWSCloseDate": "",
                "aWSAccountOwnerName": "am",
                "aWSAccountOwnerEmail": "am@amazon.com",
                "awsAccountId": "123456789123",
                "additionalComments": "Acomments",
                "apnCrmUniqueIdentifier": ""  
            }
        ]
    }

#Error duplicate PartnerCRMID
@pytest.fixture
def opportunity_input_uat5(execution_name):
    return {
        "version": "1",
        "spmsId": conf.spmid,
        "opportunities": [
            {
                "useCase": "Business Applications",
                "targetCloseDate": "2024-06-30",
                "projectDescription": "Automation Platform development for bank. Need support in understanding customer requirements and any background on their cloud projects",
                "postalCode": "84133",
                "partnerProjectTitle": "UAT123456",
                "partnerPrimaryNeedFromAws": "Deal support",
                "partnerCrmUniqueIdentifier": "UAT123456",
                "industry": "Financial Services",
                "expectedMonthlyAwsRevenue": 100.0,
                "deliveryModel": "SaaS or PaaS",
                "customerWebsite": "ally.com",
                "customerCompanyName": "Ally Segall",
                "country": "United States",
                "state": "Alaska" , 
                "IsOppFromMarketingActivity" : "No",
                "primaryContactPhone": "5555555",
                "primaryContactLastName": "PartnerSalesRepLastName",
                "primaryContactFirstName": "PartnerSalesRepFirstName",
                "primaryContactEmail": "PartnerSalesRepLastName@partner.com",
                "customerTitle": "mr",
                "customerPhone": "99999999",
                "customerLastName": "customerlastname",
                "customerFirstName": "customerfirstname",
                "customerEmail": "cust@cust.com"
            }
        ]
    }

@pytest.fixture
def opportunity_success_result():
    return {
        "success": "ALL",
        "isApiError": False,
        "inboundApiResults": [
            {
                "partnerCrmUniqueIdentifier": None,
                "isSuccess": True,
                "errors": None,
                "apnCrmUniqueIdentifier": "L80446"
            }
        ],
        "apiErrors": None
    }


@pytest.fixture
def opportunity_success_failed():
    return {
        "success": "NONE",
        "spmsId": "123456",
        "isApiError": False,
        "inboundApiResults": [
            {
                "partnerCrmUniqueIdentifier": "OP004149",
                "isSuccess": False,
                "errors": [
                    "User not found for Opportunity Owner email:xyz.abc@test.com"
                ],
                "apnCrmUniqueIdentifier": None
            }
        ],
        "fileName": "opportunity-inbound/test-2020-05-28T01:21:20.json",
        "fileApnProcessedDT": "2020-05-28T15:21:22.331Z",
        "apiErrors": None
    }


@pytest.fixture
def execution_name():
    str_date = datetime.now().strftime("%Y%d%m%H%M%S")
    test_name = os.environ.get(
        'PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

    name = f"{test_name}_{str_date}"
    return name


@pytest.fixture(autouse=True, scope="module")
def step_function_arn():
    global STEPFUNCTION_ARN
    for step_function in sfn.list_state_machines()['stateMachines']:
        if step_function['name'] == f"AIF-Partner-to-AWS-{conf.stage}":
            STEPFUNCTION_ARN = step_function['stateMachineArn']
    if STEPFUNCTION_ARN == None:
        raise Exception(
            "Not Found Step Function for AIF-Partner-to-AWS")


def trigger_execution(execution_name, input):
    global STEPFUNCTION_ARN
    counter = 20
    result = sfn.start_execution(
        stateMachineArn=STEPFUNCTION_ARN, input=json.dumps(input), name=execution_name)
    try:
        for i in range(counter):
            result = sfn.describe_execution(
                executionArn=result["executionArn"])
            if result['status'] != "RUNNING":
                execution_history = sfn.get_execution_history(
                    executionArn=result['executionArn'], reverseOrder=True)
                return execution_history
            time.sleep(2)
        else:
            raise TimeoutError("StepFunction still running")
    except:
        sfn.stop_execution(executionArn=result['executionArn'])
        raise


class TestOpportunityFromPartner:

    def test_invalid_opportunity_type(self, execution_name):

        result = trigger_execution(execution_name, {
            "test": "hi"
        })
        assert result['events'][0]['executionFailedEventDetails']['error'] == 'UnknownUpdateType'

    def test_lead_opportunity_type_not_implemented(self, execution_name):

        result = trigger_execution(execution_name, {
            "leads": "something"
        })
        assert result['events'][0]['executionFailedEventDetails']['error'] == 'LeadNotImplemented'

    def test_opportunity_partner_crm_id_is_integer(self, execution_name, opportunity_input,  opportunity_success_result, request):
        opportunity_input['opportunities'][0]['partnerCrmUniqueIdentifier'] = 123
        result = trigger_execution(execution_name, opportunity_input)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'

    def test_opportunity_aws_revenue_is_string(self, execution_name, opportunity_input,  opportunity_success_result, request):
        opportunity_input['opportunities'][0]['expectedMonthlyAwsRevenue'] = "5k"
        result = trigger_execution(execution_name, opportunity_input)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'

    def test_opportunity_missed_mandatory_field(self, execution_name, opportunity_input,  opportunity_success_failed, request):

        del opportunity_input['opportunities'][0]['useCase']

        result = trigger_execution(execution_name, opportunity_input)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'
        assert "Validation Error: Value is required. Use Case" in result[
            'events'][0]['executionSucceededEventDetails']['output']


class TestUATIntegrationTests:
    #1 
    def test_uat_1_partner_imports_new_opp(self, execution_name, opportunity_input,  opportunity_success_result, request):

        result = trigger_execution(execution_name, opportunity_input)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'
        assert "true" in result['events'][0]['executionSucceededEventDetails']['output']
    
    #2 Create with all mandatory fields + partner sales contact details
    def test_uat_2_partner_imports_new_opp(self, execution_name, opportunity_input_uat2,  opportunity_success_result, request):

        result = trigger_execution(execution_name, opportunity_input_uat2)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'
        assert "true" in result['events'][0]['executionSucceededEventDetails']['output']
    
    #3 Create with all mandatory fields + partner sales contact + customer contact details
    def test_uat_3_partner_imports_new_opp(self, execution_name, opportunity_input_uat3,  opportunity_success_result, request):

        result = trigger_execution(execution_name, opportunity_input_uat3)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'
        assert "true" in result['events'][0]['executionSucceededEventDetails']['output']

    #4 Create with all possible fields
    def test_uat_4_partner_imports_new_opp(self, execution_name, opportunity_input_uat4,  opportunity_success_result, request):

        result = trigger_execution(execution_name, opportunity_input_uat4)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'
        assert "true" in result['events'][0]['executionSucceededEventDetails']['output']

    #5 Error duplicate PartnercrmUniqueId
    def test_uat_5_partner_imports_new_opp(self, execution_name, opportunity_input_uat5,  opportunity_success_result, request):

        result = trigger_execution(execution_name, opportunity_input_uat5)

        assert "Record is not editable." in result['events'][0]['executionSucceededEventDetails']['output']

    def test_uat_3_update_fields(self, execution_name, opportunity_input,  opportunity_success_result, request):

        opps = opportunity_input['opportunities'][0]

        opps['partnerCrmUniqueIdentifier'] = "The_second"
        opps['targetCloseDate'] = (
            datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        opps['expectedMonthlyAwsRevenue'] = float(randint(1, 10000))
        opps['nextStep'] = f"Latest Update: {datetime.now()}"

        opportunity_input['opportunities'][0] = opps
        result = trigger_execution(execution_name, opportunity_input)

        assert result['events'][0]['type'] == 'ExecutionSucceeded'
        assert "true" in result['events'][0]['executionSucceededEventDetails']['output']
