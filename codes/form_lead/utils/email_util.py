import re
from email.mime.text import MIMEText
import boto3
from email.mime.multipart import MIMEMultipart
from botocore.exceptions import ClientError

def send_raw_email(to_email, reply_to, subject,
                   message_text, message_html=None):
    

    SENDER = "DreamPotential <lead@dreampotential.org>" # change from email when you are in production server
    msg = MIMEMultipart('mixed')
    msg.set_charset("utf-8")
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = ", ".join(to_email)
    # msg['Reply-to'] = ",".join(reply_to)

    CHARSET = "utf-8"
    textpart = MIMEText(message_text.encode(CHARSET), 'plain', CHARSET)
    # htmlpart = MIMEText(message_html.encode(CHARSET), 'html', CHARSET)

    # Create a multipart/alternative child container.
    msg_body = MIMEMultipart('alternative')
    msg_body.attach(textpart)
    # msg_body.attach(htmlpart)

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    msg.attach(msg_body)
    # attachmensts
    # XXX remove hard coded client

    client = boto3.client(
        'ses', aws_access_key_id='AKIAU7EQAGZOOVFPYIWO',
        aws_secret_access_key='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',
        region_name='us-west-1')

    try:
        print(
            client.send_raw_email(
                RawMessage={'Data': msg.as_string()},
                Source=SENDER, Destinations=to_email))
    except Exception as e:  
        print(f"ERROR here!@!!! {e}")
