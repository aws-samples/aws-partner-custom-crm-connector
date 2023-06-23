from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer

logger = Logger()
tracer = Tracer()


@tracer.capture_lambda_handler
def lambda_handler(event, context):
    success = {}
    failures = {}
    all_results = {}
    message = ""
    subject = "ACE Import succeeded"
    for result in event:
        identifier = result['Output']['partnerCrmUniqueIdentifier']
        all_results[identifier] = result['Output']
        if result['Output']['isSuccess']:
            success[identifier] = result['Output']
        else:
            failures[identifier] = result['Output']
    if len(failures) != 0:
        subject = f"ACE Import failed for {len(failures)} opportunities"
        message += """
=======================================================
ERRORS with imported opportunities:"""
        for partner_crm_id in failures:

            message += f"""
     Partner CRM ID: '{partner_crm_id}'
        Errors: """
            for index, error in enumerate(failures[partner_crm_id]['errors']):
                message += f"""
            {index+1}: {error}\n"""

    if len(success) != 0:
        message += """
=======================================================
SUCCESSFUL imported opportunities:\n"""
        for partner_crm_id in success:
            message += f"   Partner CRM ID: '{partner_crm_id}' APN CRM ID: '{success[partner_crm_id]['apnCrmUniqueIdentifier']}'\n"
    print(message)

    return {
        "subject": subject,
        "message": message,
        "opportunities": {
            "imported": len(success),
            "failed": len(failures)
        },
        "result": all_results

    }
