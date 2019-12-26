import pandas as pd 
import numpy as np
import re
from type_dict import type_dict
from brand_dict import brand_dict
from dist_dict import dist_dict
from owner_dict import owner_dict
from lat_dict import lat_dict
from lng_dict import lng_dict
from zoom_dict import zoom_dict
import sqlite3

# Read original csv file
df = pd.read_csv("../tfidf_whiskey/archive.csv")
df_getnames = pd.read_csv("../cf_whiskey/similars.csv", index_col=0)

whiskey_names = df_getnames.index.values.tolist()

# Rename columns for ease of use
new_names =  {'Whisky Name': 'whiskey',
    'Reviewer Rating': 'rating',
    'Whisky Region or Style': 'type',
    'Reviewer\'s Reddit Username': 'username'}
df.rename(columns=new_names, inplace=True)

# Delete rows with Community username
df = df[~df.username.str.endswith('Community')]

# Delete unused and unreliable columns
df.drop(columns=["Timestamp","username","Link To Reddit Review","Date of Review","Full Bottle Price Paid"], inplace=True)

# Convert all ratings to numbers, return NaN if error
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Delete rows with no rating (were probably bad format)
df.dropna(subset=['rating'], inplace=True)

# Delete rows with ratings < 11 (typically wrong scale)
df.drop(df[df.rating < 11].index, inplace=True)

df["type"].replace(type_dict, inplace=True)

def remove_end_space(whiskey_name):
    space_re = "\s+$"
    try:
        whiskey_name = re.sub(space_re,'',whiskey_name)
    except:
        return whiskey_name
    return whiskey_name

df["whiskey"] = df["whiskey"].apply(remove_end_space)

# make dataframe groups sorted by whiskeys
db_name = df.groupby(df.whiskey)

#initiate empty lists
all_whiskeys = []
num_reviews = []
average_ratings = []
std_devs = []
types = []

# loop through each group (whiskey) to combine the reviews
for name,grouped in db_name:
    #get number of entries in the group
    num_reviews.append(grouped.shape[0])
    #pull stats based on groups
    all_whiskeys.append(name)
    average_ratings.append(grouped.rating.mean())
    std_devs.append(grouped.rating.std())
    
    temp = grouped.type.agg(lambda x:x.value_counts().index[0])
    types.append(temp)

df2 = pd.DataFrame()
df2['whiskey'] = all_whiskeys
df2['reviews'] = num_reviews
df2['average'] = average_ratings
df2['std_dev'] = std_devs
df2['type'] = types

df2 = df2[df2["whiskey"].isin(whiskey_names)]
df2 = df2.round(2)

df2.set_index("whiskey", drop=True, inplace=True)

df2["brand"] = df2.index.map(brand_dict, na_action='ignore')
df2["dist"] = df2["brand"].map(dist_dict, na_action='ignore')
df2["owner"] = df2["brand"].map(owner_dict, na_action='ignore')
df2["lat"] = df2["dist"].map(lat_dict, na_action='ignore')
df2["lng"] = df2["dist"].map(lng_dict, na_action='ignore')
df2["zoom"] = df2["dist"].map(zoom_dict, na_action='ignore')

df2.to_csv("stats.csv")
df2.to_sql("stats", sqlite3.connect("../whiskey.db"), if_exists='replace')