from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer

logger = Logger()
tracer = Tracer()


@tracer.capture_lambda_handler
def lambda_handler(event, context):

    print(event)

    event = enforce_types(event)
    return event


def enforce_types(event: dict):

    tmp = []
    for opportunity in event['opportunities']:
        for key in opportunity.keys():
            if key == "expectedMonthlyAwsRevenue":
                try:
                    opportunity["expectedMonthlyAwsRevenue"] = int(float(
                        opportunity["expectedMonthlyAwsRevenue"])
                    )
                except Exception as ex:
                    # Raise Validation Exception from ACE Team
                    opportunity["expectedMonthlyAwsRevenue"] = -1
            else:
                opportunity[key] = str(opportunity[key])
        tmp.append(opportunity)

    event['opportunities'] = tmp
    return event
