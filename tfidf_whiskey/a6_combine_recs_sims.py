import pandas as pd

df1 = pd.read_csv("recommendations.csv")
df2 = pd.read_csv("similarities.csv")

for i in range(1, 101):
    df1[f'TF_Similarity_{i}'] = df2[f'TF_Similarity_{i}']

df1.to_csv("TF_sims1.csv", index=False)