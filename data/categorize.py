import pandas as pd
from textblob import TextBlob

df = pd.read_csv('word_count.csv')

print(df.columns)

def get_sentiment(word):
    analysis = TextBlob(word)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'

df['Sentiment'] = df['word'].apply(get_sentiment)  

df.to_csv('word_count_with_sentiment.csv', index=False)

print("Sentiment analysis completed and saved to 'word_count_with_sentiment.csv'.")
