import pandas as pd
import re
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import nltk

# Download the WordNet data for lemmatization
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger_eng')

def clean_text(text):
    re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text.lower()

def get_wordnet_pos(treebank_tag):
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

def lemmatize_word(word):
    lemmatizer = WordNetLemmatizer()
    pos = get_wordnet_pos(nltk.pos_tag([word])[0][1])
    return lemmatizer.lemmatize(word, pos)

# Load the CSV file
df = pd.read_csv('data.csv')

# Clean the Comment column
df['Cleaned_Comment'] = df['Comment'].apply(lambda x: clean_text(x))

# Tokenize the cleaned text
df['Tokens'] = df['Cleaned_Comment'].apply(lambda x: x.split())

# Flatten the list of tokens
tokens = [word for sublist in df['Tokens'].tolist() for word in sublist]

# Lemmatize and count words
words = [lemmatize_word(word) for word in tokens]
word_counts = pd.Series(words).value_counts().reset_index()
word_counts.columns = ['word', 'count']

# Save the result to a new CSV file
word_counts.to_csv('word_counts.csv', index=False)
