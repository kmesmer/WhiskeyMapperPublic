import pandas as pd 
import numpy as np
import re

# Read original csv file
df = pd.read_csv("archive.csv")

# Rename columns for ease of use
new_names =  {'Whisky Name': 'whiskey',
    'Link To Reddit Review': 'link',
    'Reviewer\'s Reddit Username': 'username'}
df.rename(columns=new_names, inplace=True)

# Delete rows with Community username
df = df[~df.username.str.endswith('Community')]

# Delete unused and unreliable columns
df.drop(columns=["Timestamp","Date of Review","Full Bottle Price Paid","username","Reviewer Rating","Whisky Region or Style"], inplace=True)

def get_subid(link):
    term = 'comments/.*?/'
    try:
        id_text = re.search(term, link).group()
        sub_id = id_text.split('/')[1]
    except:
        sub_id = ''
    return sub_id

# Add column for submission IDs using function from get_subid
sub_ids = df['link'].apply(get_subid)
df['sub_id'] = sub_ids
df.drop(df[df.sub_id == ""].index, inplace=True)

# Remove reviews with multiple whiskeys because format is unreliable
df.drop_duplicates(subset ="sub_id", keep = False, inplace = True)

# Save cleaned dataframe to csv
df.to_csv("archive_clean.csv", index=False)