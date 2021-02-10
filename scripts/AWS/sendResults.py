import bucket_utils
import sqs_utils

queue_url = 'https://sqs.us-east-1.amazonaws.com/838549581352/SendResults.fifo'
bucket_name = 'results-bucket-big-data-6'

def run(file_name, bucket_file_name):
    print("Uploading '" + file_name + "' file on '" + bucket_name + "' bucket as '" + bucket_file_name + ".")
    print()
    bucket_utils.upload_file(file_name=file_name, bucket_name=bucket_name, object_name=bucket_file_name)


    message_attributes={
                'Title': {
                    'DataType': 'String',
                    'StringValue': 'SendResults'
                },
                'BucketFileName': {
                    'DataType': 'String',
                    'StringValue': bucket_file_name
                }
            }
    print('Sending message to send results ...')
    print()
    result = sqs_utils.send_message(queue_url=queue_url, message_attributes=message_attributes)

    print(result)
    print()
    print('Done.')