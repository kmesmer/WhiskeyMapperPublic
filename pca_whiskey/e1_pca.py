import pandas as pd 
import numpy as np
from sklearn.decomposition import PCA
import sqlite3
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("../flavor_whiskey/words_per_review.csv", index_col=0)

df_types = pd.read_csv("../stats_whiskey/stats.csv", index_col=0)
type_dict = dict(zip(df_types.index, df_types.type))

x = df.values
whiskey_names = df.index

pca = PCA(n_components=3)

principalComponents = pca.fit_transform(x)
print(pca.explained_variance_ratio_)

pcadf = pd.DataFrame(data = principalComponents, columns = ['Component_1', 'Component_2', 'Component_3'], index=whiskey_names)

pcadf['type'] = pcadf.index.map(type_dict)

scaler = MinMaxScaler()
pcadf["Component_1"] = scaler.fit_transform(pcadf[["Component_1"]])
pcadf["Component_2"] = scaler.fit_transform(pcadf[["Component_2"]])
pcadf["Component_3"] = scaler.fit_transform(pcadf[["Component_3"]])

pcadf.to_csv("pca.csv")
pcadf.to_sql("pca", sqlite3.connect("../whiskey.db"), if_exists='replace')