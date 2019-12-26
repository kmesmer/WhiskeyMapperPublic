import pandas as pd
import numpy as np
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("archive_clean.csv")

df = df.drop_duplicates(['whiskey','username'])

# discarding unused whiskies
recs_df = pd.read_csv("../tfidf_whiskey/TF_sims2.csv")
col_list = recs_df["whiskey"].tolist()
df = df[df.whiskey.isin(col_list)]

df = df.pivot(index='whiskey', columns='username', values='rating').fillna(0)

sims = cosine_similarity(df)

sims[np.isclose(sims, 1)] = np.nan

df2 = pd.DataFrame( data=sims,
                    columns=df.index.values,
                    index=df.index.values)

scaler = QuantileTransformer(n_quantiles=10, output_distribution='uniform')
scaled_df = scaler.fit_transform(df2)

df3 = pd.DataFrame( data=scaled_df,
                    columns=df.index.values,
                    index=df.index.values)

df3["whiskey"] = df2.index.values

df3.to_csv("CF_sims1.csv")