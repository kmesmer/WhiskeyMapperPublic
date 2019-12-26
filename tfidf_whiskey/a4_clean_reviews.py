import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import re
import imp
from fix_words import word_dict

def token_master(review):
    cleaned_tokens = clean_words(review)
    lemm_tokens = tag_stopword_lemmatize(cleaned_tokens)
    return lemm_tokens

def clean_words(review):
    try:
        words = word_tokenize(review)
    except:
        return []
    alphabet = '[^a-zA-Z\']'
    new_words = []
    for word in words:
        new_word = re.sub(alphabet,'',word)
        if len(new_word) > 0:
            new_words.append(new_word)
    return new_words

def convert_pos(tag):
    if tag.startswith('J') or tag.startswith('S'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
def tag_stopword_lemmatize(token_review):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tags = nltk.pos_tag(token_review)
    new_words = []
    for tag in tags:
        if tag[0] not in stop_words:
            w_tag = convert_pos(tag[1])
            lem_word = lemmatizer.lemmatize(tag[0],w_tag)
            if wordnet.synsets(lem_word):
                new_words.append(lem_word)
    return new_words

if __name__ == "__main__":
    df = pd.read_csv("reviews_cut.csv", usecols=["whiskey","review"])

    reviews = df["review"].tolist()

    count = 1

    for i in range(len(reviews)):
        reviews[i] = token_master(reviews[i])
        print(count)
        count += 1

    df["review"] = reviews

    df = df[df["review"].astype(str).str.len() > 5]

    for lst in df["review"]:
      for ind, item in enumerate(lst):
          if item in word_dict:
              lst[ind] = word_dict[item]

    df.to_csv("reviews_clean.csv", index=False)