import pandas as pd
import numpy as np
import sqlite3

df1 = pd.read_csv("combined_sims.csv")

whiskey_list = df1["whiskey"].tolist()

for i in range(1,51):
    df1[f"Wtg_Avg_Sim_{i}"] = np.nan

for i in range(len(df1["whiskey"])):
    for j in range(1,51):
        TF = df1.loc[df1['whiskey'] == whiskey_list[i],f"TF_Similarity_{j}"].values[0]
        CF = df1.loc[df1['whiskey'] == whiskey_list[i],f"CF_Similarity_{j}"].values[0]
        Flav = df1.loc[df1['whiskey'] == whiskey_list[i],f"Flavor_Similarity_{j}"].values[0]
        Wpr = df1.loc[df1['whiskey'] == whiskey_list[i],f"Words_Similarity_{j}"].values[0]
        wtd_avg = TF * 0.0 + CF * 0.15 + Flav * 0.25 + Wpr * 0.6
        df1.loc[df1['whiskey'] == whiskey_list[i],f"Wtg_Avg_Sim_{j}"] = wtd_avg

for j in range(1,51):
    df1.drop(columns=[f"TF_Similarity_{j}",f"CF_Similarity_{j}",f"Flavor_Similarity_{j}",f"Words_Similarity_{j}"], inplace=True)

for x in range(1, 51):
    df1[f'Whiskey_{x}'] = list(zip(df1[f'Wtg_Avg_Sim_{x}'], df1[f'Reco_{x}']))

for y in range(1,51):
    df1.drop(columns=[f"Reco_{y}",f"Wtg_Avg_Sim_{y}"], inplace=True)

df2 = df1

df2.drop(columns= "whiskey", inplace=True)
sort_df = df2.values
sort_df.sort(axis=1)
df3 = pd.DataFrame(sort_df, index=whiskey_list, columns=df2.columns)

df3 = df3.iloc[:, ::-1]

for i in range(1,21):
    z = 51 - i
    df3[f"Match_{i}"], df3[f"Reco_{i}"] = zip(*df3[f"Whiskey_{z}"])

for j in range(1,51):
    df3.drop(columns=f"Whiskey_{j}", axis=1, inplace=True)

df3.index.name='whiskey'

df3.to_csv("similars.csv", index=True)
df3.to_sql("similars", sqlite3.connect("../whiskey.db"), if_exists='replace')