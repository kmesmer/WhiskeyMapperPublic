import pandas as pd
import numpy as np
import requests
import praw
import sys

def extract_reviews(dataframe, re_client_id, re_client_secret, re_username, re_pw):
    # Initialize counter
    count = 0
    total = dataframe.shape[0]
    
    # Get the sub_ids as a list
    sub_ids = dataframe["sub_id"].tolist()

    # Initialize an empty list of reviews
    reviews = []
    
    # Initiate PRAW
    reddit = praw.Reddit(   client_id= re_client_id,\
                            client_secret = re_client_secret,\
                            username = re_username, \
                            password = re_pw,
                            user_agent= 'v1')
    
    # Iterate through the submission ids
    for i in sub_ids:
        review = ''
        try:
            sub = reddit.submission(id = i)
            s_author = sub.author.name
        except:
            reviews.append(review)
            continue
        
        # Add selftext to review
        sub_text = sub.selftext
        if len(sub_text) > 0:
            review = review + sub_text + ' \n'

        # Add OP topline comments
        for comment in sub.comments:
            try:
                if comment.author.name == s_author:
                    review = review + comment.body + '\n'
            except:
                continue
        
        reviews.append(review)
        
        # Show success rate
        count_str = f"extracted {str(count)}/{str(total)} reviews"
        sys.stdout.write("\r{}".format(count_str))
        count += 1

    # Return list of reviews to be added to dataframe    
    return reviews

if __name__ == "__main__":
    re_client_id = "[This is private]"
    re_client_secret = "This is private"
    re_username = "This is private"
    re_pw = "This is private"

    # Read original csv file
    df = pd.read_csv("archive_clean.csv")

    # Add reviews to dataframe
    reviews = extract_reviews(df, re_client_id, re_client_secret, re_username, re_pw)
    df["review"] = reviews

    # Save new table to csv
    df.to_csv("reviews_raw.csv", index=False)