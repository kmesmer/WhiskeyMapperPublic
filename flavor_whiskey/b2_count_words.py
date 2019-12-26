import pandas as pd
import numpy as np
import re
from flavor_map import flavor_map

df = pd.read_csv("collapsed.csv")

#remove whiskeys not in recommendations
df_getnames = pd.read_csv("../tfidf_whiskey/TF_sims2.csv", index_col=0)
whiskey_names = df_getnames.index.values.tolist()
df = df[df["whiskey"].isin(whiskey_names)]

keys = flavor_map.keys()
whiskeys = df["whiskey"]
x = 0

for i in whiskeys:
    for j in keys:
        temp = str(f"\'{j}\'")
        count = len(re.findall(temp, str(df.loc[df["whiskey"] == i, "review"].values)))
        df.loc[df["whiskey"] == i, j] = count
    print(x)
    x += 1

df.drop("review", axis=1, inplace=True)

df.to_csv("word_counts.csv", index=False)