import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


""" Récupérer le corpus de textes """
df = pd.read_json('data.json')
df_reindexed = df.set_index('Id')


""" Catégories par identifiant && Fusion dataframe """
df_lbl = pd.read_csv("label.csv")
df_reindexed['category'] = df_lbl['Category']


""" Récupérer les catégories (association nom / Id) """
df_cat_names = pd.read_csv("categories_string.csv")
df_cat_names.rename(columns = {'0' : 'name', '1' : 'Id'}, inplace = True)


""" Affichage données """
header = df_reindexed.head(20)
footer = df_reindexed.tail(20)

print("Corpus\n")
print(header)
print("\n" + "....." + "\n")
print(footer)

print("\nCategories\n")
print(df_cat_names)


""" Vectorizer training """
# vectorizer = TfidfVectorizer()
# vectorizer.fit(corpus)
# tf_Idf = vectorizer.transform(corpus)


""" Convert the sparse output matrix to dense matrix """
# print(tf_Idf.toarray())
