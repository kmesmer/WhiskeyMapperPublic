import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("TF_sims1.csv")

scaler = MinMaxScaler()

#The following code scales the cosine similarities, however we will ultimately discard the tf_idf similarities anyway
for i in range(1,101):
    scaler.partial_fit(df[[f"TF_Similarity_{i}"]])

for i in range(1,101):
    df[f"TF_Similarity_{i}"] = scaler.transform(df[[f"TF_Similarity_{i}"]])

for j in range(51,101):
    df.drop(columns=[f"TF_Similarity_{j}", f"Reco_{j}"], inplace=True)

df = df.round(4)

df.to_csv("TF_sims2.csv", index=False)