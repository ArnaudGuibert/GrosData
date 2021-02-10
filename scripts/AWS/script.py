import receivePredict
import sendResults
import predict
import os

predict_file_name = 'predict.csv'
results_file_name = 'results.csv'

def delete_file(file_name):
    os.remove(file_name)

if __name__ == "__main__":
    while(True):
        print('[START]')
        print()
        bucket_object_name = receivePredict.getBucketFileName()
        receivePredict.download_predict(bucket_object_name, predict_file_name)
        predict.predict(predict_file_name, results_file_name)
        delete_file(predict_file_name)
        sendResults.run(results_file_name, results_file_name)
        delete_file(results_file_name)
        print('[END]')
        print()