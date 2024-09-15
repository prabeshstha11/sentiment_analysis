import pandas as pd
import re
from nltk.corpus import wordnet, stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download the WordNet data for lemmatization
nltk.download('wordnet')
"""
WordNet is a large database of English words.
"""
nltk.download('stopwords')
"""
get stopwords dataset
"""
nltk.download('averaged_perceptron_tagger_eng')
"""
It identifies the structure of a sentence (nouns, verbs, etc.)
"""

stop_words = set(stopwords.words('english'))

def clean_text(text):
    # removes url from text
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)

    # remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # remove non ascii characters (emojis, any other words)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.lower()

# lemmatization: changing, changed, changes to change
def get_wordnet_pos(treebank_tag):
    # J, V, N, R are tags (treebank)
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    
def remove_stop_words(tokens):
    return [word for word in tokens if word not in stop_words]

def lemmatize_word(word):
    lemmatizer = WordNetLemmatizer()
    """
    WordNetLemmatizer() is a class in the NLTK library that uses the WordNet lexical database to look up the root word. 
    """

    # for taking root position words
    pos = get_wordnet_pos(nltk.pos_tag([word])[0][1])
    return lemmatizer.lemmatize(word, pos)

df = pd.read_csv('data.csv')

df['Cleaned_Comment'] = df['Comment'].apply(lambda x: clean_text(x))
df['Tokens'] = df['Cleaned_Comment'].apply(lambda x: remove_stop_words(x.split()))
tokens = [word for sublist in df['Tokens'].tolist() for word in sublist]

words = [lemmatize_word(word) for word in tokens]
word_counts = pd.Series(words).value_counts().reset_index()
word_counts.columns = ['word', 'count']

word_counts.to_csv('word_count.csv', index=False)
