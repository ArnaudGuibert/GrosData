import bucket_utils
import sqs_utils

starting_queue_url = 'https://sqs.us-east-1.amazonaws.com/838549581352/StartPredicting.fifo'
predict_bucket_name = 'predict-bucket-big-data-6'

def getBucketFileName():
    print('Waiting for queue starting message ...')
    print()

    message = sqs_utils.receive_message(starting_queue_url)
    print('Received and deleted message: %s' % message)
    print()
    print()

    bucket_object_name = message['MessageAttributes']['BucketFileName']['StringValue']
    print('Bucket file name: %s' % bucket_object_name)
    return bucket_object_name

def download_predict(bucket_object_name, file_name):
    print("Downloading predict file '" + bucket_object_name + "' from bucket '" + file_name + "' as '" + file_name + "' ...")
    print()

    bucket_utils.download_file(object_name=bucket_object_name, bucket_name=predict_bucket_name, file_name=file_name)

    print("File " + bucket_object_name + " downloaded and renamed to " + file_name + ".")
    print()

    bucket_utils.delete_file(object_name=bucket_object_name, bucket_name=predict_bucket_name)

    print("Deleting predict file '" + bucket_object_name + "' on bucket '" + predict_bucket_name + "' ...")
    print()