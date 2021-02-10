import sqs_utils
import bucket_utils
import csv
import os
from pymongo import MongoClient

results_queue_url = 'https://sqs.us-east-1.amazonaws.com/838549581352/SendResults.fifo'
BUCKET_NAME = 'results-bucket-big-data-6'

MONGO_URL = 'mongodb://localhost:27017'

FILE_NAME= 'results.csv'



def getBucketFileName():
    print('Waiting for queue sending results ...')
    print()

    message = sqs_utils.receive_message(results_queue_url)
    print('Received and deleted message: %s' % message)
    print()

    bucket_object_name = message['MessageAttributes']['BucketFileName']['StringValue']
    print('Bucket file name: %s' % bucket_object_name)


    return bucket_object_name

def downloadResults(bucket_object_name):
    print("Downloading predict file '" + bucket_object_name + "' from bucket '" + FILE_NAME + "' as '" + FILE_NAME + "' ...")
    print()

    bucket_utils.download_file(object_name=bucket_object_name, bucket_name=BUCKET_NAME, file_name=FILE_NAME)

    print("File " + bucket_object_name + " downloaded and renamed to " + FILE_NAME + ".")
    print()

    bucket_utils.delete_file(object_name=bucket_object_name, bucket_name=BUCKET_NAME)

    print("Deleting file '" + bucket_object_name + "' on bucket '" + BUCKET_NAME + "' ...")
    print()


def injectResultsInMongo():
    print('Injecting data in MongoDB ...')
    client = MongoClient(MONGO_URL)
    
    db = client['BigDataDB']
    collection_resume = db['resume']

    with open('results.csv', newline='', encoding='utf-8') as csvfile:
        #reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            #print(row['description'])
            json_resume = {'description': row['description'], 'job_id' : row['job_id']}
            collection_resume.insert_one(json_resume)

    print("Results injected in MongoDB")
    print()

def removeResultsFile():
    os.remove(FILE_NAME)

while(True):
    print('[START]')
    print()
    bucket_object_name = getBucketFileName()
    downloadResults(bucket_object_name)
    injectResultsInMongo()
    removeResultsFile()
    print('[END]')
    print()