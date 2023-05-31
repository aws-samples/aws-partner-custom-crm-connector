import boto3
import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer

logger = Logger()
tracer = Tracer()


@tracer.capture_lambda_handler
def lambda_handler(event, context):

    print(event)

    assume_role_session = get_session_with_assume_role(event['RoleArn'])

    bucket = assume_role_session.resource(
        "s3").Bucket(event['Bucket'])

    bucket.put_object(
        Key=event['Key'],
        ACL=event['ACL'],
        Body=json.dumps(event['Body'])
    )


def get_session_with_assume_role(arn: str) -> boto3.Session:
    sts = boto3.client('sts')
    response = sts.assume_role(
        RoleArn=arn,
        RoleSessionName="write-ace-outboundlambda"
    )
    new_session = boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                                aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                                aws_session_token=response['Credentials']['SessionToken'])

    return new_session
