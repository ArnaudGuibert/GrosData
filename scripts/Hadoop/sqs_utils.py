import boto3
from datetime import datetime


def send_message(queue_url, message_body="none", message_attributes={}, message_group_id="message", message_deduplication_id=""):
    # Send message to SQS queue

    if not message_deduplication_id:
        message_deduplication_id = str(datetime.timestamp(datetime.now()))

    sqs = boto3.client('sqs')

    if not message_attributes:
        print("Change message_attributes")
        message_attributes = {
            'Title': {
                'DataType': 'String',
                'StringValue': 'NoTitle'
            },
            'Author': {
                'DataType': 'String',
                'StringValue': 'NoAuthor'
            }
        }

    
    return sqs.send_message(
            QueueUrl=queue_url,
            MessageDeduplicationId=message_deduplication_id,
            MessageAttributes=message_attributes,
            MessageGroupId=message_group_id,
            MessageBody=message_body
        )    

def receive_message(queue_url):
    # Receive message from SQS queue

    sqs = boto3.client('sqs')

    while 1:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            AttributeNames=[
                'All'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=43200, # Max value
            WaitTimeSeconds=1
        )
        if 'Messages' in response.keys():
            #print("Yes")
            break
        #else:
            #print("No")

    #print("[RESPONSE]="+str(response))
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )

    #print('Received and deleted message: %s' % message)
    return message
    