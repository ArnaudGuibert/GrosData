import logging
import boto3
from botocore.exceptions import ClientError

def upload_file(file_name, bucket_name, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def download_file(object_name, bucket_name, file_name=None):
    """Download a file from an S3 bucket
    """

    # If file_name was not specified, use object_name
    if file_name is None:
        file_name = object_name
    
    s3_client = boto3.resource('s3')
    try:
        s3_client.Bucket(bucket_name).download_file(object_name, file_name)
        #print('Results received')
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object " + object_name + " does not exist.")
        else:
            raise

def delete_file(object_name, bucket_name):
    """Delete a file on an S3 bucket
    """

    s3_client = boto3.resource('s3')
    try:
        s3_client.Object(bucket_name, object_name).delete()
        #s3_client.Bucket(bucket_name).delete_file(object_name)
        #print('Results received')
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object " + object_name + " does not exist.")
        else:
            raise