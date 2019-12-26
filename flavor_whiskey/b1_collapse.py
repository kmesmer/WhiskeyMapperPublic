import pandas as pd
import numpy as np
import re
from ast import literal_eval

def remove_end_space(whiskey_name):
    # remove space at end of whiskey names
    space_re = "\s+$"
    try:
        whiskey_name = re.sub(space_re,'',whiskey_name)
    except:
        return whiskey_name
    return whiskey_name

def fix_columns(db, column = 'whiskey', convert = True):
    # if list saved as string in CSV, convert back to list
    db[column] = db[column].apply(remove_end_space)
    if convert == True:
        db["review"] = db["review"].apply(literal)
    return db

def literal(x):
    #convert strings to lists, convert NaN to empty list
    if type(x) == float:
        return []
    else:
        return literal_eval(x)

def final_df(db, group = "whiskey", fix_cols = True, columns = ["whiskey"], convert = True):
    #combine review words for each whiskey
    if fix_cols == True:
        for i, column in enumerate(columns):
            if i > 0:
                #only convert strings to list once
                convert = False        
            db = fix_columns(db, column = column, convert = convert)
    
    # make dataframe groups sorted by whiskeys
    db_name = db.groupby(group)
    
    #initiate empty lists
    all_whiskeys = []
    all_words = []
    entries = []
    
    # loop through each group (whiskey) to combine the reviews
    for name,grouped in db_name:
        #get number of entries in the group
        entries.append(grouped.shape[0])
        #append whiskey name
        all_whiskeys.append(name)
    
        words = []

        for line in grouped.iterrows():
            words += line[1]["review"]
        
        all_words.append(words)

    new_df = pd.DataFrame()
    new_df['whiskey'] = all_whiskeys
    new_df['review'] = all_words
    new_df['# reviews'] = entries

    return new_df

if __name__ == "__main__":
    df = pd.read_csv("../tfidf_whiskey/reviews_clean.csv")

    df2 = df[df["review"].astype(str).str.len() > 5]

    df3 = final_df(df2, group = "whiskey", fix_cols = True, columns = ["whiskey"], convert = True)

    df3.to_csv("collapsed.csv", index=False)