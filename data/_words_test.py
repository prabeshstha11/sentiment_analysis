# seperate the word as positive or negative
from textblob import TextBlob

def get_sentiment(word):
    analysis = TextBlob(str(word))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity < 0:
        return 'negative'
    else:
        return 'neutral'
    
while(True):
    word = input("enter word: ")
    print(get_sentiment(word))