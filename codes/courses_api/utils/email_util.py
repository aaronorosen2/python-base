import boto3
from botocore.exceptions import ClientError
import random

def generate_code():
    return str(random.randrange(1000, 9999))

def send_email_code():
    send_email_code.verification_code = generate_code()
    return send_email_code.verification_code

def send_email(to_email):
    SENDER = "DreamPotential <lead@dreampotential.org>"
    RECIPIENT = to_email
    AWS_REGION = "us-west-1"
    CHARSET = "UTF-8"
    SUBJECT = "Verify your email address"
    
    BODY_HTML = """
    <html>
        <head></head>
        <body>
            <h1> Verify your login </h1>
            <p> Below is your one time passcode: </p>
            <p><b>{verification_code}</b></p>
            <p> if you didn't request this, you can ignore his email or let us know. </p>
            <p> Thanks! </p>
            <p> DreamPotential Team </p>
        </body>
    </html>
    """            

    client = boto3.client('ses', aws_access_key_id='AKIAU7EQAGZOOVFPYIWO',
            aws_secret_access_key='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', region_name=AWS_REGION)

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML.format(verification_code=send_email_code.verification_code),
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
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])