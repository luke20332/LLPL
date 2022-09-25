from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#using some sent analysis libraries to do sentiment analysis.

# TB build on nltk
# VS just sentiment analysis, smaller than TB

# have 2 reviews positive and negative
# may not be clear, can be confusing (sarcasm may be present for example)

# if we have confidence levels, we can determine how accurate it is, and how good guesses are.

# sample string, turned into a textblob object
#analysis = TextBlob("TextBlob sure looks like it has some interesting features!")
#print(dir(analysis))
# dir gives all the operations we can perform on the Textblob object

#print(analysis.translate(from_lang='en', to='es'))

#print(analysis.tags)
# tags are what Textblob deems each word as
# NNP = proper noun, ie TextBlob
# JJ= adjective
# building noun phrases, or look at what is being spoken about

# if positive, we determine that textblob has positive sentiment due to the secondary noun features, ie interesting features are good

#print(analysis.sentiment)
# returns 2 values - polarity and subjectivity.
# polarity = -1 to 1
# subjectivity = 0 to 1 (obj to subj)

# polarity is basically what we are looking for = how positive or negative the sentiment is 


# copied from sentdex tutorial

"""

pos_count = 0 # thinks positive, may be right or wrong
pos_correct = 0 # actually correct

with open("C:/Users/lukem/Documents/projects/LLPL/sentiment/positive.txt","r") as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line) # use that line as a textblob object
        if analysis.sentiment.subjectivity > 0.8:
          # if the line is mostly objective (not an opinion), throw out others (too subj)
          if analysis.sentiment.polarity > 0: # if it thinks positive (it is)
              pos_correct += 1 # increment the correct counter
          pos_count +=1

neg_count = 0 
neg_correct = 0

with open("C:/Users/lukem/Documents/projects\/LLPL/sentiment/negative.txt", "r") as f:
  for line in f.read().split('\n'):
    analysis = TextBlob(line)
    if analysis.sentiment.subjectivity > 0.8:
      if analysis.sentiment.polarity <= 0: # thinks negative
        neg_correct +=1 # add to correctly guessed
      neg_count += 1 


print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count)) 
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))

"""

#analysis.sentiment.polarity just takes the polarity value of that given sentiment of the textblob object

# we are opening the files and reading them in line by line. if the polarity is above 0, then it should be positive. if correct, add 1 to correct. if wrong, we make total pos count incremented

# we then summarise the total correctly guessed positive or correct guesses out of them all, and return the accuracy of the sentiment analyser.
# positive acc is 71%, negative is 56%. not overly accurate/

# improving it
# play with where the line for neutral zone being drawn.
# ie above 0.2 not 0.
# we are fairly weighted towards positive, play with that to get them equal.
# making it 0.2 makes it heavily weighted towards negative (80%).
# 0.1 = 60, 68.

# could take subjectivity into account.
# so before we take a positive or negative sentiment of a line into account, we first demonstrate that the line is subjective. if it is, we throw it out as it is more opinion based.

# doing this with lines with less than 0.3 (more objective), then negative accuracy goes up a lot, positive goes down a lot. sample size has reduced by a lot

# making it more subjective, (>0.8), means we get less samples, barely any, but the accuracy is a lot higher overall, around 70%.
# dont want to be too close to subjective or objective, dont know how to value subjectivity.

# Vader sentiment
# build it similarly,

analyzer = SentimentIntensityAnalyzer()
# a SIA object, use to perform SA.


vs = analyzer.polarity_scores("VADER Sentiment looks interesting, I have high hopes!")
# vs object is using the SIA object, finding the polarity scores on the string
print(vs)

# {'neg': 0.0, 'neu': 0.463, 'pos': 0.537, 'compound': 0.6996}
# neg is the amound of negative sentiment
# neutral, positive.
# compound is a metric for finding a unidimensional measure of sentiment.

"""
positive sentiment: compound score >= 0.5
neutral sentiment: (compound score > -0.5) and (compound score < 0.5)
negative sentiment: compound score <= -0.5
"""

# again copied from sentdex

"""threshold = 0.5

pos_count = 0
pos_correct = 0

with open("C:/Users/lukem/Documents/projects/LLPL/sentiment/positive.txt","r") as f:
    for line in f.read().split('\n'):
      # make a vs object using a line
        vs = analyzer.polarity_scores(line)
        if vs['compound'] >= threshold or vs['compound'] <= -threshold:
           if vs['compound'] > 0:
            pos_correct += 1
           pos_count +=1


neg_count = 0
neg_correct = 0

with open("C:/Users/lukem/Documents/projects/LLPL/sentiment/negative.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if vs['compound'] >= threshold or vs['compound'] <= -threshold:
          if vs['compound'] <= 0:
              neg_correct += 1
          neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))

"""

# again, slightly weighted towards the correct way, but not exaclty acceptable since positive is 70%, negative is 57%.

# between -0.5 and 0.5 is neutral, so we should alter for this.
# to do so, we only account for the guess of a positive or negative sentiment if the compound of the sentiment is outside of the neutral zone (-0.5 to 0.5)

# accuracy is now 87 and 50.


# what if we dont want compound.
# for negative, we want more negative than positive, but also not much positive either.


"""

pos_count = 0
pos_correct = 0

with open("C:/Users/lukem/Documents/projects/LLPL/sentiment/positive.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['neg'] > 0.1: # if neg findings not more than 0.1, 
            if vs['pos']-vs['neg'] > 0: # if the positive findings - negative is still >0, then we account for it as positive.
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with open("C:/Users/lukem/Documents/projects/LLPL/sentiment/negative.txt","r") as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['pos'] > 0.1: # not a lot of positive sentiment
            if vs['pos']-vs['neg'] <= 0: # if more negative than positive
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))

"""

# by being more specific with what we want, ie for positive, if there is not a lot of negative sentiment, and the positive sentiment outweighs the negative, then we will count it.

# this has given a very good accuracy level, with the majority of the samples still being considered.

# this was wrong, as we accounted for lines that were both negative and positive, suing the =. this means the accuracy is now around 0.5. bad.

# can go with greater than 0 for the positive requirement, and less than or equal to 0 for the negative requirement, 

# we never tested textblob with a neutral zone, instead, we gave a fixed point of being positive or negative and tested against that.

pos_count = 0
pos_correct = 0

with open("C:/Users/lukem/Documents/projects/LLPL/sentiment/positive.txt","r") as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        # positive sentiment
        if analysis.sentiment.polarity >= 0.1:
            if analysis.sentiment.polarity > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with open("C:/Users/lukem/Documents/projects/LLPL/sentiment/negative.txt","r") as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        if analysis.sentiment.polarity <= -0.1:
            if analysis.sentiment.polarity <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))

# now we have no overlap. no neutral ones are being considered.

# get 100% accuracy, with barely any samples, even when we lower the threshold requirement (get more samples though)
# also if threshold is 0.0001

# reason is the 0, as a lot of things have 0 sentiment polarity, causing some issues.

# textblob may be better, but vs is a lot quicker






