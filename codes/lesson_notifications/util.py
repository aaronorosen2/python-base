import boto3
from botocore.exceptions import ClientError
import random
import json
import requests

from web import settings


def send_email(to_email, lesson_name, lesson_id):
    SENDER = "DreamPotential <lead@dreampotential.org>"
    RECIPIENT = to_email
    AWS_REGION = "us-east-2"
    CHARSET = "UTF-8"
    SUBJECT = "Lesson Completed"
    
    BODY_HTML = """
    <html>
        <head></head>
        <body>
            <h1> Lesson Completed </h1>
            <p> Below lesson has been completed: </p>
            <p><b>Lesson Name: {lesson_name}</b></p>
            <p><b>Lesson Id: {lesson_id}</b></p>
            <p> One new response has been recieved for the lesson. </p>
            <p> Thanks! </p>
            <p> DreamPotential Team </p>
        </body>
    </html>
    """            
    client = boto3.client('ses', aws_access_key_id=getattr(settings,'EMAIL_AWS_ACCESS_KEY_ID', None),
            aws_secret_access_key=getattr(settings, 'EMAIL_AWS_SECRET_ACCESS_KEY', None), region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    *RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML.format(lesson_name=lesson_name, lesson_id=lesson_id),
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        print(e, e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


def send_slack_notification(channel, lesson_id, lesson_name):
    
    message = "Lesson Completed\n Below lesson has been completed:\n Lesson Id: {lessonId} \n Lesson Name: {lessonName}".format(lessonId=lesson_id, lessonName=lesson_name)

    body = {"text": "%s" % message,
            'username': 'Lesson-Agent',
            'channel': 'C03J2UB8S8Z'}
    headers = {'Authorization': 'Bearer xoxb-790630255906-1844871421842-FFFWwP6KQT2eIsjTBHA8fsUR', 'Content-type': 'application/json'}
    resp = requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=json.dumps(body))
    print(resp.text)
