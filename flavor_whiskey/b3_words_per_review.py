import pandas as pd
import numpy as np
import re
from flavor_map import flavor_map

df = pd.read_csv("word_counts.csv")

keys = flavor_map.keys()

for i in keys:
    df[f"{i}"] = df[f"{i}"] / df["# reviews"]

df.drop("# reviews", axis=1, inplace=True)

df.set_index("whiskey", drop=True, inplace=True)

df.to_csv("words_per_review.csv")