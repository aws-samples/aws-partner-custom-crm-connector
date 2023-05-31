from datetime import datetime
import os
import json
import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools.logging.correlation_paths import S3_OBJECT_LAMBDA
from aws_lambda_powertools.utilities.data_classes.s3_event import S3Event
import email
from email.message import Message

sfn = boto3.client('stepfunctions')
s3_bucket = boto3.resource("s3").Bucket(
    os.environ['UPLOAD_BUCKET'])
sns_topic = boto3.resource("sns").Topic(os.environ["SNS_TOPIC_ARN"])
UPLOAD_DIRECTORY = os.environ['UPLOAD_DIRECTORY']
logger = Logger()
tracer = Tracer()


@logger.inject_lambda_context(correlation_id_path=S3_OBJECT_LAMBDA)
def lambda_handler(event, context):
    try:
        print(event)

        event = S3Event(event)

        print("Load email from S3: " + event.object_key)

        msg = load_email_from_s3(event.object_key)

        check_if_validated_sender(msg)

        str_date = datetime.now().strftime("%Y%d%m%H%M%S")
        type_of_email = get_type(msg)

        print("Import Type: " + type_of_email)

        for attachment in msg.get_payload():
            name = attachment.get_filename()
            if name:
                print("Processing Attachment: " + name)
                name = name.replace(" ", "")
                destination = f"{UPLOAD_DIRECTORY}/{type_of_email}/{str_date}-{name}"
                print("Uploading attachment to " + destination)
                s3_object = s3_bucket.put_object(Key=destination, Body=attachment.get_payload(
                    decode=True)
                )
                tmpevent = {
                    "EMAIL": {
                        "From": msg['From'],
                        "To": msg['To'],
                        "Subject": msg['Subject'],
                        "Date": msg['Date']
                    },
                    "S3": {
                        "Bucket":  os.environ['UPLOAD_BUCKET'],
                        "Key": destination
                    }
                }
                print("Execute Step Function: " + os.environ['STEP_FUNCTION_ARN'])
                json_event = json.dumps(tmpevent)
                print(json_event)
                response = sfn.start_execution(
                    stateMachineArn=os.environ['STEP_FUNCTION_ARN'],
                    input=json_event,
                    name=f"{str_date}-{name}"
                )
    finally:
        delete_object_from_s3(event.object_key)


def load_email_from_s3(key) -> Message:
    s3_object = s3_bucket.Object(key=key)
    body = s3_object.get()['Body'].read()
    msg = email.message_from_bytes(body)

    return msg


def check_if_validated_sender(msg):
    email_adress = os.environ.get("VALID_EMAIL_ADDRESS")
    from_email = msg['From'].split(
        "<")[-1].split(">")[0]  # Strip down to plane email
    print(f"Validate eMail if sender {from_email}  in {email_adress}")
    if os.environ.get('IS_VALIDATE_EMAIL_ACTIVE') == "True" and \
            from_email.lower() not in email_adress.lower():
        sns_topic.publish(
            Subject="ACE inbound eMail BLOCKED. Invalid Sender",
            Message=f"""
            eMail Send from {from_email} is not {email_adress}
            """)
        raise Exception(f"EMAIL: {from_email} not in validated")


def get_type(msg):
    if "lead" in msg["To"]:
        return "lead"
    else:
        return "opportunity"


def delete_object_from_s3(s3key):
    s3_client = boto3.client('s3')

    print("Purge file")

    response = s3_client.delete_object(
        Bucket=os.environ['UPLOAD_BUCKET'],
        Key=s3key
    )

    print(response)
    return response
