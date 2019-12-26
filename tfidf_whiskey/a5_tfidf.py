import pandas as pd 
import numpy as np
import tfidf_funcs as tf
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

df1 = pd.read_csv("reviews_clean.csv")
df2 = tf.fix_columns(df1, column = 'whiskey', convert = False)
df3 = tf.final_df(df2, group = 'whiskey')
df3.sort_values(['# reviews'], ascending=False, inplace = True)
df3.reset_index(inplace = True)
df3 = df3[df3['# reviews'] >= 8]

vector = tf.tf_idf(df3, features= False, max_df = 0.8, min_df = .02)

print(str(len(vector.toarray()[0])) + ' terms')

lsa_vector = tf.latent_semantic(vector)

print(str(len(lsa_vector)) + ' terms')

cos = cosine_similarity(lsa_vector)

recommendation_df = tf.get_top20(cos, whiskeys=df3["whiskey"])

recommendation_df.to_csv("recommendations.csv", index=False)

similarities = tf.relative_similarity(cos, whiskeys=df3["whiskey"])

similarities.to_csv("similarities.csv", index=False)