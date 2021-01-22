import pandas as pd
import matplotlib.pyplot as plt

import csv

from sklearn.feature_extraction.text import TfidfVectorizer


""" Récupérer le corpus de textes """
df = pd.read_json('data.json')
df_reindexed = df.set_index('Id')


""" Catégories par identifiant && Fusion dataframe """
df_lbl = pd.read_csv("label.csv")
df_reindexed['category'] = df_lbl['Category']


""" Récupérer les catégories dans un dictionnaire (association Id / nom) """
with open('categories_string.csv', mode = 'r') as infile:
    reader = csv.reader(infile)
    classes = { int(rows[1]) : rows[0] for rows in reader }


""" Group by categories """
total = len(df_reindexed.index)
grouped = df_reindexed.groupby(['category', 'gender'], as_index = False).count()
grouped.rename(columns = { 'description' : 'count' }, inplace = True)


""" Affichage données """
def show_stuff(df, classes, grouped):
    # first / last rows
    header = df_reindexed.head(20)
    footer = df_reindexed.tail(20)

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


show_stuff(df_reindexed, classes, grouped)


""" Vectorizer training """
# vectorizer = TfidfVectorizer()
# vectorizer.fit(corpus)
# tf_Idf = vectorizer.transform(corpus)


""" Convert the sparse output matrix to dense matrix """
# print(tf_Idf.toarray())



