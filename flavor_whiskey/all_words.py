import pandas as pd
import numpy as np
from ast import literal_eval
from collections import Counter

df = pd.read_csv("reviews_clean.csv")

words = df["review"].tolist()

flat = []

for i in words:
    i = i.replace("'", "")
    i = i.replace("[", "")
    i = i.replace("]", "")
    i = i.split(", ")
    for j in i:
        flat.append(j)

word_counts = Counter(flat)

df = pd.DataFrame.from_dict(word_counts, orient='index').reset_index()

df.to_csv("all_words.csv", index=False)