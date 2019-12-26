import pandas as pd 
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("flavors.csv", index_col=0)

sims = cosine_similarity(df)

sims[np.isclose(sims, 1)] = np.nan

df2 = pd.DataFrame( data=sims,
                    columns=df.index.values,
                    index=df.index.values)

df2["whiskey"] = df.index.values

df2.to_csv("flavor_sims.csv")