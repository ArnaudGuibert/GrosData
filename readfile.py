import pandas as pd
import matplotlib.pyplot as plt

import csv

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# A faire la premiere fois
# nltk.download('punkt')
# nltk.download('stopwords')


def pre_processing(dataframe):
    # preprocessing
    cachedStopWords = stopwords.words("english") + [ ",", "." , "'" ]
    stemmer = SnowballStemmer("english")
    dataframe['description'] = dataframe['description'].apply(lambda x: pre_process_text(x, cachedStopWords, stemmer))


def pre_process_text(text, cachedStopWords, stemmer):
    # To lower case
    text_lower = text.lower()
    # Text to word array
    word_array = word_tokenize(text_lower)
    # Remove stop words
    word_array = [word for word in word_array if word not in cachedStopWords]
    # Stemming
    word_array = [stemmer.stem(word) for word in word_array]
    # Word array to text
    return ' '.join(word_array)


def show_repartition(dataframe, classes):
    # Group by categories
    total = len(dataframe.index)
    grouped = dataframe.groupby(['category', 'gender'], as_index = False).count()
    grouped.rename(columns = { 'description' : 'count' }, inplace = True)
    
    # first / last rows
    header = dataframe.head(5)

    # print first and last lines
    print("Corpus Header\n")
    print(header)
    print("")

    # show graph result
    values = [ [ None for i in range(2)] for j in range(len(classes.keys())) ]

    for i, row in grouped.iterrows():
        # nb from this groupby
        count = row['count']

        # category id
        category = row['category']

        # gender
        if row['gender'] == "M":
            gender = 0 # man
        else:
            gender = 1 # woman

        # update values
        values[category][gender] = count

    # plot histogram
    index = classes.values()
    data = pd.DataFrame(values, index = index, columns = ["M", "F"])
    data.plot(kind = 'bar')
    plt.show()


def tf_idf_machine_learning(dataframe, withPreProcessing = False):
    # preprocessing
    if withPreProcessing:
        print("Start pre processing...")
        pre_processing(dataframe)
        print("End of pre processing\n")

    # fonction pour le machine learning TF-IDF
    X = dataframe['description']
    y = dataframe['category']

    # split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 42, test_size = 0.3)

    # TF-IDF vectorizer + LinearSVC
    text_clf = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LinearSVC()),
    ])

    print("Start of model fitting...")
    text_clf.fit(X_train, y_train)
    print("End of model fitting\n")

    # make predictions on test data
    predictions = text_clf.predict(X_test)

    # print metrics n' stuff
    print("\nAccuracy score: % s " % accuracy_score(y_test, predictions))
    
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
    show_repartition(df_reindexed, classes)

    # first TF-IDF model test
    tf_idf_machine_learning(df_reindexed, True)



### FIN DE SCRIPT ###
