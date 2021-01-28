import pandas as pd
import matplotlib.pyplot as plt

import csv

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer


def show_repartition(dataframe, classes):
    # Group by categories
    total = len(dataframe.index)
    grouped = dataframe.groupby(['category', 'gender'], as_index = False).count()
    grouped.rename(columns = { 'description' : 'count' }, inplace = True)
    
    # first / last rows
    header = dataframe.head(20)
    footer = dataframe.tail(20)

    # print first and last lines
    print("Corpus\n")
    print(header)
    print("\n" + "....." + "\n")
    print(footer)

    # print dictionary of categories
    print("\nCategories\n")
    print(classes)

    # show graph result
    print("\nRepartition")
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


def tf_idf_machine_learning(dataframe):
    # fonction pour le machine learning TF-IDF
    X = dataframe['description']
    y = dataframe['category']

    # train / test / split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 42, test_size = 0.3)

    # declare & train TF-IDF vectorizer
    raise NotImplementedError


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


### FIN DE SCRIPT ###
