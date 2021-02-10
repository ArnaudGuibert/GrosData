#-------------------------------------------------------------------------------
# Name:        predict
# Purpose:     predict results using model
# 
# Author:      @ArnaudGuibert
#
# Created:     17/01/2021
# Copyright:   (c) arnaud guibert 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np
import pandas as pd

from joblib import dump, load


def load_as_series(filename):
    # return Series from predict.csv
    return pd.read_csv(filename)['description']


def predict_classes(X_predict):
    # load model
    modelSVC = load("models/tfidf_save_monogram.joblib")

    # predict classes
    predictions = modelSVC.predict(X_predict)
    return pd.Series(predictions)


if __name__ == "__main__":
    # load CSV
    X_predict = load_as_series("in&out/predict.csv")

    # predict
    job_ids = predict_classes(X_predict)

    # write return CSV
    data = pd.concat( { "description" : X_predict, "job_id" : job_ids } , axis = 1 )
    data.to_csv("in&out/results.csv", index = None)


### FIN DE SCRIPT ###
