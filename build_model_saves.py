import csv
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nltk
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from joblib import dump, load


def pre_processing(dataframe):
    # preprocessing
    stemmer = WordNetLemmatizer()
    dataframe['description'] = dataframe['description'].apply(lambda x: pre_process_text(x, stemmer))


def pre_processing_text(document, stemmer):
    # Remove all the special characters
    document = re.sub(r'\W', ' ', document)
    
    # remove all single characters
    document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
    
    # Remove single characters from the start
    document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
    
    # Substituting multiple spaces with single space
    document = re.sub(r'\s+', ' ', document, flags=re.I)
    
    # Removing prefixed 'b'
    document = re.sub(r'^b\s+', '', document)
    
    # Converting to Lowercase
    document = document.lower()
    
    # Lemmatization
    document = document.split()
    document = [stemmer.lemmatize(word) for word in document]
    
    # Word array to text
    return ' '.join(document)


def show_repartition(dataframe, classes):
    # print title
    print(title + "\n")

    # Create dataframe grouped by category and gender
    grouped = dataframe.groupby(['category', 'gender']).size().unstack('gender')
    grouped['disparate_impact'] = grouped[['M', 'F']].max(axis='columns') / grouped[['M', 'F']].min(axis='columns')
    grouped = grouped.rename(index = classes)

    # Show dataframe
    print(grouped)
    print("")
    
    """
    # [ OPTIONAL ] Show repartition graph
    graph = grouped.drop('disparate_impact', axis = 1)
    graph.plot(kind = 'bar')
    plt.show()
    """


def build_tf_idf_save(dataframe, classes, ngram, withPreProcessing = False):
    # preprocessing
    if withPreProcessing:
        print("Start of pre processing...")
        pre_processing(dataframe)
        print("End of pre processing\n")

    # show initial gender data repartition
    show_repartition(dataframe, classes, 'Repartition of full set')

    # fonction pour le machine learning TF-IDF
    Xd = dataframe['description']
    Xg = dataframe['gender']
    y = dataframe['category']
    
    # split data -- keep the same random_state and test_size for index matching
    Xd_train, Xd_test, y_train, y_test = train_test_split(Xd, y, random_state = 42, test_size = 0.3)
    _ , Xg_test , _ , _ = train_test_split(Xg, y, random_state = 42, test_size = 0.3)

    # show gender data repartition on test values
    df_test_true = pd.DataFrame( { 'gender' : Xg_test, 'category' : y_test } )
    show_repartition(df_test_true, classes, 'True repartition of test set')

    # TF-IDF vectorizer + LinearSVC
    modelSVC = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words = stopwords.words('english'), ngram_range = (ngram, ngram)), ('clf', LinearSVC()),
    ])

    print("Start of model fitting...")
    modelSVC.fit(Xd_train, y_train)
    print("End of model fitting\n")

    # name of config model file
    if withPreProcessing:
        if ngram == 1:
            name = "models/tfidf_save_monogram_prepro.joblib"
        else:
            name = "models/tfidf_save_bigram_prepro.joblib"
    else:
        if ngram == 1:
            name = "models/tfidf_save_monogram.joblib"
        else:
            name = "models/tfidf_save_bigram.joblib"

    # save model
    print("Saving model...")
    dump(modelSVC, name)

    # make predictions on test data
    predictions = modelSVC.predict(Xd_test)

    # show repartition for predicted test values
    df_test_predicted = pd.DataFrame(predictions, index = list(df_test_true.index), columns = ['category'])
    df_test_predicted['gender'] = df_test_true['gender']
    show_repartition(df_test_predicted, classes, 'Predicted repartition of test set')
    
    # print metrics 'n stuff
    print("\nAccuracy score: %s" % accuracy_score(y_test, predictions))
    
    print("\nConfusion matrix:\n")
    print(confusion_matrix(y_test, predictions))
    
    print("\nClassification report:\n")
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    # get category names as dictionary
    with open('categories_string.csv', mode = 'r') as infile:
        reader = csv.reader(infile)
        classes = { int(rows[1]) : rows[0] for rows in reader }

    # get text corpus and merge dataframes
    df = pd.read_json('data.json')
    df_reindexed = df.set_index('Id')

    df_lbl = pd.read_csv("label.csv")
    df_reindexed['category'] = df_lbl['Category']
    
    # train model, show F1 / other scores
    for ngram in [ 1 , 2 ]:
        for withPreProcessing in [ True , False ]:
            build_tf_idf_save(df_reindexed, classes, ngram, withPreProcessing)


### FIN DE SCRIPT ###
