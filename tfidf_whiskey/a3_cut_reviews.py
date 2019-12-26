import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
import re
import imp

df = pd.read_csv("reviews_raw.csv", usecols=["whiskey","review"])

reviews = df["review"].tolist()

#The following code removes preambles and anything that comes after the final rating
for i in range(len(reviews)):
    reviews[i] = str(reviews[i])
    reviews[i] = reviews[i].lower()
    if re.search('appearance[:-]|appearance [:-]|\*appearance\*|color[:-]|color [:-]|\*color\*|colour[:-]|colour [:-]|\*colour\*', reviews[i]) is not None:
        reviews[i] = re.split('appearance[:-]|appearance [:-]|\*appearance\*|color[:-]|color [:-]|\*color\*|colour[:-]|colour [:-]|\*colour\*', reviews[i])[-1]
    elif re.search('nose[:-]|nose [:-]|\*nose\*|[\*\s]n[:-]', reviews[i]) is not None:
        reviews[i] = re.split('nose[:-]|nose [:-]|\*nose\*|[\*\s]n[:-]', reviews[i])[-1]
    else:
        pass

for i in range(len(reviews)):
    reviews[i] = reviews[i].lower()
    if re.search('/100', reviews[i]) is not None:
        reviews[i] = re.split('/100', reviews[i])[0]
    elif re.search('\*score|score:|\*rating|rating:', reviews[i]) is not None:
        reviews[i] = re.split('\*score|score:|\*rating|rating:', reviews[i])[0]
    else:
        pass

df["review"] = reviews

df.to_csv("reviews_cut.csv", index=False)