import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
  print(f"Received data from form: {event}")
  
  sender = "Hello <hello@yourdomain.com>"
  recipient = "sales@yourdomain.com"
  subject = f"New Customer: {event['name']}"

  with open('template.txt') as file:
    text = file.read()
  text = text.replace('_name', event['name'])
  text = text.replace('_email', event['email'])
  text = text.replace('_message', event['message'])
  
  with open('template.html') as file:
    html = file.read()
  html = html.replace('_name', event['name'])
  html = html.replace('_email', event['email'])
  html = html.replace('_message', event['message'])

  charset = "UTF-8"
  
  aws_region = "us-east-1"
  client = boto3.client('ses',region_name=aws_region)
  
  try:
    response = client.send_email(
      Destination={
        'ToAddresses': [
          recipient,
        ],
      },
      Message={
        'Body': {
          'Html': {
            'Charset': charset,
            'Data': html,
          },
          'Text': {
            'Charset': charset,
            'Data': text,
          },
        },
        'Subject': {
          'Charset': charset,
          'Data': subject,
        },
      },
      Source=sender,
    )
  except ClientError as e:
    print(e.response['Error']['Message'])
  else:
    print(f"Email sent, Message ID: {response['MessageId']}")
