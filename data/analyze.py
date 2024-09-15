import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

df = pd.read_csv('final.csv')


""" count of good is 3 then -> good good good"""
df['text'] = df.apply(lambda row: f"{row['word']} " * row['count'], axis=1)

text_data = df['text']
sentiments = df['Sentiment']

sentiments = sentiments.map({'positive': 1, 'neutral': 0, 'negative': -1})

# split dataset for testing and training
# 20% used for testing, 80% for training
X_train, X_test, y_train, y_test = train_test_split(text_data, sentiments, test_size=0.2, random_state=42, stratify=sentiments)

# Create a pipeline with CountVectorizer and Naive Bayes classifier
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model with zero_division parameter
print(classification_report(y_test, y_pred, zero_division=0))

# Predict sentiment for the overall video

"""
i love movie but it is bad

[-, 1, 0, -, -, -, -1]
"""
def aggregate_sentiments(df, model):
    predictions = []
    for row in df.iterrows():
        text = f"{row['word']} " * row['count']
        sentiment = model.predict([text])[0]
        predictions.extend([sentiment] * row['count'])
    
    sentiment_counts = pd.Series(predictions).value_counts()

    """
    this is the hashmap containing
    1(positive) -> count
    -1(negative) -> count

    if count is not found then returns 0 else returns count
    """
    if sentiment_counts.get(1, 0) > sentiment_counts.get(-1, 0):
        return 'positive'
    elif sentiment_counts.get(-1, 0) > sentiment_counts.get(1, 0):
        return 'negative'
    else:
        return 'neutral'

overall_sentiment = aggregate_sentiments(df, model)
print(f'Overall Sentiment of the Video: {overall_sentiment}')
