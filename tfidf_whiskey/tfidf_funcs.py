import pandas as pd
from ast import literal_eval
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import random
import re

######## TF-IDF, LSA, Cosine Similarity

def tf_idf(df,features = False,max_df=.8,min_df=.01, \
           stop_words = [],ngram = 1,norm='l2'):
    tf_matrix = df["review"].apply(lambda x: ' '.join(x))
    vectorizer = TfidfVectorizer(lowercase = False, max_df = max_df,min_df = min_df,\
                    norm = norm,ngram_range=(0,ngram),stop_words = stop_words)
    vector = vectorizer.fit_transform(tf_matrix)
    return vector

def latent_semantic(vector, explained_var = 0.8):
    #calculate the vector length of tfidf and create a numpy
    len_vector = len(vector.toarray()[0])
    
    #create a range of n_components to try
    n_com_range = np.arange(100,len_vector,50)
    
    #create a for loop iterating increasing n_components until explained 
    #variance is satisfied
    for n_com in n_com_range:
        lsa = TruncatedSVD(n_components = n_com, n_iter =10)
        data_lsa = lsa.fit_transform(vector)    
        exp_var = sum(lsa.explained_variance_)
        if exp_var > explained_var:
            break    
    return data_lsa

def get_top20(similarity_matrix, whiskeys, top_recs = 100):
    #make a new dataframe and populate it with Whiskey names
    new_db = pd.DataFrame()
    new_db['whiskey'] = whiskeys
    
    #Create ranked indices of cosine similarities
    ranks = np.argsort(similarity_matrix)
    
    #Create an empty list of twenty entries to Top 20 similar whiskey names
    sim_twenty = [[] for _ in range(top_recs)]
    
    #iterate through each whiskey similarity ranks
    for whiskey in ranks:
        #Find the indices of top 20 most similar whiskeys.
        top_20 = whiskey[-1*top_recs-1:-1][::-1]
        for i,rank in enumerate(top_20):
            #get the name of the similar whiskey
            sim_name = whiskeys[rank]
            sim_twenty[i].append(sim_name)
    for i in range(top_recs):
        #Populate the database with similar whiskey names
        name = 'Reco_' + str(i+1)
        new_db[name] = sim_twenty[i]
    return new_db

def relative_similarity(similarity_matrix, whiskeys, top_recs = 100):
    """This function calculates relative similarity of output whiskies"""
    new_db = pd.DataFrame()
    new_db['whiskey'] = whiskeys
    
    #Create ranked indices of cosine similarities
    rank_twenty = [[] for _ in range(top_recs)]
    ranks = np.argsort(similarity_matrix)
    for idx,whiskey in enumerate(ranks):
        #Get indicies of the top 20 most similar whiskeys
        top_20 = whiskey[(-1*top_recs)-1:-1][::-1]
        for i,rank in enumerate(top_20):
            # if i == 0:
            #     top_sum = np.array(similarity_matrix[idx][rank])
            #calculate relative similarity
            curr_sum = np.array(similarity_matrix[idx][rank])
            # rel_sum = round(100 *curr_sum / top_sum,1)
            # also changed following line to curr_sum from rel_sum
            rank_twenty[i].append(curr_sum)
    for i in range(top_recs):
        #Populate the database with relative ranks
        name = "TF_Similarity_" + str(i+1)
        new_db[name] = rank_twenty[i]
    return new_db

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
            
def get_int(x):
    try:
        return int(x)
    except:
        return np.nan