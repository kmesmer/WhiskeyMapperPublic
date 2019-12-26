import pandas as pd
import numpy as np
import re
import sqlite3

df = pd.read_csv("words_per_review.csv", index_col = 0)

df.drop(columns=["sweet", "rye", "light", "dark", "clear", "pale", "straw", "gold", "yellow", "amber", "deep", "copper", "tawny", "mahogany", "brown", "big", "heavy", "strong"], inplace=True)

arr = np.argsort(-df.values, axis=1)
df = pd.DataFrame(df.columns[arr], index=df.index)

df = df.iloc[:,0:20]

whiskey_list = df.index.values

df2 = pd.read_csv("words_per_review.csv", index_col = 0)

for i in range(20):
    df[f"count_{i}"] = np.nan

for i in range(len(whiskey_list)):
    for j in range(20):
        df.loc[whiskey_list[i],f"count_{j}"] = df2.loc[whiskey_list[i],df.loc[whiskey_list[i],j]]

df.to_csv("top_20.csv")
df.to_sql("top_20", sqlite3.connect("../whiskey.db"), if_exists='replace')