import pandas as pd
import matplotlib.pyplot as plt

import time
import csv

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

from joblib import dump, load

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# A faire (juste la première fois)
# nltk.download('punkt')
# nltk.download('stopwords')


def pre_processing(dataframe):
    # preprocessing
    cachedStopWords = stopwords.words("english") + [ "," , "." , "'" ]
    stemmer = SnowballStemmer("english")
    dataframe['description'] = dataframe['description'].apply(lambda x: pre_process_text(x, cachedStopWords, stemmer))


def pre_process_text(text, cachedStopWords, stemmer):
    # Remove stop words
    word_array = [ word for word in word_tokenize(text.lower()) if word not in cachedStopWords ]
    
    # Stemming
    word_array = [ stemmer.stem(word) for word in word_array ]
    
    # Word array to text
    return ' '.join(word_array)


def show_repartition(dataframe, classes, title = 'Gender repartition by category'):
    # print title
    print(title + "\n")

    # Create dataframe grouped by category and gender
    grouped = dataframe.groupby(['category', 'gender']).size().unstack('gender')
    grouped['disparate_impact'] = grouped[['M', 'F']].max(axis='columns') / grouped[['M', 'F']].min(axis='columns')
    grouped = grouped.rename(index = classes).sort_values('disparate_impact', ascending=False)

    # Show dataframe
    print(grouped)
    print("")
    
    # [ OPTIONAL ] Show repartition graph
    """
    graph = grouped.drop('disparate_impact', axis = 1)
    graph.plot(kind = 'bar')
    plt.show()
    """


def tf_idf_machine_learning(dataframe, classes, withPreProcessing = False):
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
        ('tfidf', TfidfVectorizer()),
        ('clf', LinearSVC()),
    ])

    print("Start of model fitting...")
    modelSVC.fit(Xd_train, y_train)
    print("End of model fitting\n")

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
    # get text corpus
    df = pd.read_json('data.json')
    df_reindexed = df.set_index('Id')
    
    # get categories and merge dataframes
    df_lbl = pd.read_csv("label.csv")
    df_reindexed['category'] = df_lbl['Category']
    
    # get category names as dictionary
    with open('categories_string.csv', mode = 'r') as infile:
        reader = csv.reader(infile)
        classes = { int(rows[1]) : rows[0] for rows in reader }

    # show info on data repartition
    tf_idf_machine_learning(df_reindexed, classes, False)


"""
dump(clf, 'filename.joblib')
clf = load('filename.joblib')
"""


### FIN DE SCRIPT ###
