import pandas as pd
import numpy as np

df1 = pd.read_csv("../tfidf_whiskey/TF_sims2.csv")
df2 = pd.read_csv("CF_sims1.csv")
df3 = pd.read_csv("../flavor_whiskey/flavor_sims.csv")
df4 = pd.read_csv("../flavor_whiskey/wpr_sims.csv")

whiskey_list = df1["whiskey"].tolist()

for i in range(1,51):
    df1[f"CF_Similarity_{i}"] = np.nan
    df1[f"Flavor_Similarity_{i}"] = np.nan
    df1[f"Words_Similarity_{i}"] = np.nan

for i in range(len(df1["whiskey"])):
    for j in range(1,51):
        temp = df2.loc[df2['whiskey'] == whiskey_list[i], df1.loc[df1['whiskey'] == whiskey_list[i], f"Reco_{j}"]].values[0]
        df1.loc[df1['whiskey'] == whiskey_list[i],f"CF_Similarity_{j}"] = temp
        temp2 = df3.loc[df3['whiskey'] == whiskey_list[i], df1.loc[df1['whiskey'] == whiskey_list[i], f"Reco_{j}"]].values[0]
        df1.loc[df1['whiskey'] == whiskey_list[i],f"Flavor_Similarity_{j}"] = temp2
        temp3 = df4.loc[df4['whiskey'] == whiskey_list[i], df1.loc[df1['whiskey'] == whiskey_list[i], f"Reco_{j}"]].values[0]
        df1.loc[df1['whiskey'] == whiskey_list[i],f"Words_Similarity_{j}"] = temp3

df1.to_csv("combined_sims.csv", index=False)