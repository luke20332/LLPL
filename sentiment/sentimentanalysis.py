from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#using some sent analysis libraries to do sentiment analysis.

# TB build on nltk
# VS just sentiment analysis

# have 2 reviews positive and negative
# may not be clear, can be confusing (sarcasm may be present)

# if we have confidence levels, we can determine how accurate it is, and how good guesses are


analysis = TextBlob("TextBlob sure looks like it has some interesting features!")
#print(dir(analysis))
#print(analysis.translate(from_lang='en', to='es'))

#print(analysis.tags)
# tags are what Textblob deems each word as
# NNP = proper noun, ie TextBlob
# JJ= adjective

# if positive, we determine that textblob has positive sentiment due to the secondary noun features, ie interesting features are good

print(analysis.sentiment)
# returns 2 values - polarity and subjectivity.
# polarity = -1 to 1
# subjectivity = 0 to 1 (obj to subj)
# 

