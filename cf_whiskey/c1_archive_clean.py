import pandas as pd 
import numpy as np
import re

# Read original csv file
df = pd.read_csv("../tfidf_whiskey/archive.csv", usecols=["Whisky Name", "Reviewer's Reddit Username", "Reviewer Rating"])

# Rename columns for ease of use
new_names =  {'Whisky Name': 'whiskey',
    'Reviewer\'s Reddit Username': 'username',
    'Reviewer Rating': 'rating'}
df.rename(columns=new_names, inplace=True)

# Delete rows with Community username
df = df[~df.username.str.endswith('Community')]

# Convert all ratings to numbers, return NaN if error
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Delete rows with no rating (were probably bad format)
df.dropna(subset=['rating'], inplace=True)

# Delete rows with ratings < 11 (typically wrong scale)
df.drop(df[df.rating < 11].index, inplace=True)

def remove_end_space(whiskey_name):
    space_re = "\s+$"
    try:
        whiskey_name = re.sub(space_re,'',whiskey_name)
    except:
        return whiskey_name
    return whiskey_name

df["whiskey"] = df["whiskey"].apply(remove_end_space)

# Save cleaned to table to csv
df.to_csv("archive_clean.csv", index=False)