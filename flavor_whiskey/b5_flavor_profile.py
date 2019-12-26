import pandas as pd
import numpy as np
from flavor_map import flavor_map
from sklearn.preprocessing import QuantileTransformer
import sqlite3

df = pd.read_csv("words_per_review.csv", index_col = 0)

flavor_names = ["Body", "Sweetness", "Honey/Vanilla", "Floral/Herbal", "Fruity", "Winey/Sherry", "Peaty/Smoky", "Medicinal/Salty", "Tobacco/Leather", "Nutty/Creamy", "Malty", "Spicy", "Wood/Cask"]

df["delicate"] = df["delicate"] * -1
df["light"] = df["light"] * -1
df["mellow"] = df["mellow"] * -1
df["astringent"] = df["astringent"] * -1
df["dry"] = df["dry"] * -1

df["Body"] = df.loc[:,"big":"weighty"].sum(axis=1)
df["Sweetness"] = df.loc[:,"astringent":"sweet"].sum(axis=1)
df["Honey/Vanilla"] = df.loc[:,"beeswax":"vanilla"].sum(axis=1)
df["Floral/Herbal"] = df.loc[:,"arugula":"wintergreen"].sum(axis=1)
df["Fruity"] = df.loc[:,"apple":"watermelon"].sum(axis=1)
df["Winey/Sherry"] = df.loc[:,"brandy":"winey"].sum(axis=1)
df["Peaty/Smoky"] = df.loc[:,"ash":"tire"].sum(axis=1)
df["Medicinal/Salty"] = df.loc[:,"acidic":"varnish"].sum(axis=1)
df["Tobacco/Leather"] = df.loc[:,"balsamic":"vinegar"].sum(axis=1)
df["Nutty/Creamy"] = df.loc[:,"almond":"walnut"].sum(axis=1)
df["Malty"] = df.loc[:,"ale":"yeast"].sum(axis=1)
df["Spicy"] = df.loc[:,"allspice":"spicy"].sum(axis=1)
df["Wood/Cask"] = df.loc[:,"cask":"wood"].sum(axis=1)

keys = flavor_map.keys()
df.drop(labels=keys , axis=1, inplace=True)

scaler = QuantileTransformer(n_quantiles=10, output_distribution='uniform')
for i in flavor_names:
    df[f"{i}"] = scaler.fit_transform(df[[f"{i}"]])
    df[f"{i}"] = df[f"{i}"] * 10

df.to_csv("flavors.csv")
df.to_sql("flavors", sqlite3.connect("../whiskey.db"), if_exists='replace')