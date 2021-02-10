import bucket_utils
import sqs_utils

queue_url = 'https://sqs.us-east-1.amazonaws.com/838549581352/StartPredicting.fifo'
file_name = 'predict.csv'
target_file_name = 'predict.csv'
bucket_name = 'predict-bucket-big-data-6'

print('[START]')
print()
print("Uploading '" + file_name + "' file on '" + bucket_name + "' bucket as '" + target_file_name + ".")
print()
bucket_utils.upload_file(file_name=file_name, bucket_name=bucket_name, object_name=target_file_name)


message_attributes={
            'Title': {
                'DataType': 'String',
                'StringValue': 'StartPredicting'
            },
            'BucketFileName': {
                'DataType': 'String',
                'StringValue': target_file_name
            }
        }
print('Sending message to start prediction ...')
print()
result = sqs_utils.send_message(queue_url=queue_url, message_attributes=message_attributes)

print(result)
print()
print('Done. [END]')