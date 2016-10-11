from twython import Twython
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import sys

def clean_word_for_count(w): 
  w.replace(',','')
  w.replace('.','')
  return w.lower()

def get_twitter_app_authorization():
  tup = []
  with open('twitterAuthentication.txt','r') as f:
    for line in f:
      for word in line.strip().split():
        tup.append(word)
  return tup

def print_counter_words(counter, num):
  for w, c in counter.most_common(int(num)):
    print w, " ", str(c)

def filter_common_words(w):
  common_words = ['a', 'the', 'an', 'to', 'i', 'and', 'for', 'of', 'is', 'in', 'that', 'it', 'on', 'you',
      'with','are','my','if']
  if w in common_words:
    return True
  else:
    return False


# Check for correct arguments
try:
  topic = str(sys.argv[1])
except:
  print "Usage: twitterCounter.py *phrase_to_search*"
  print "To use #, you must wrap the phrase in ''"
  sys.exit(1)


auth = get_twitter_app_authorization()
twitter = Twython(auth[0], auth[1])


#search for tweets containing a phrase, count the most commonly associated words
topicwords = []
number_of_statuses = 0
for status in twitter.search(q=topic, count=1000)["statuses"]:
  number_of_statuses+=1
  user = status["user"]["screen_name"].encode('utf-8')
  text = status["text"].encode('utf-8')
  for word in text.strip().split():
    if filter_common_words(word.lower()): 
      continue
    topicwords.append(clean_word_for_count(word))
print "Most common words in ", number_of_statuses, " statuses with: ", topic
counterT = Counter(topicwords)
print_counter_words(counterT,50)


# get the tweets from a user timeline, count the most common words
kylewords = []
user_timeline = twitter.get_user_timeline(screen_name="kyletolle", count=200)
for tweet in user_timeline:
  user = tweet["user"]["screen_name"].encode('utf-8')
  time = tweet["created_at"].encode('utf-8')
  text = tweet["text"].encode('utf-8')
  for word in text.strip().split():
    if filter_common_words(word.lower()): 
      continue
    kylewords.append(clean_word_for_count(word))

print "\n@kyletolle's most used words: "
counter = Counter(kylewords)
print_counter_words(counter,50)


#Plot Kyle's most common words
#word_names = []
#word_counts = []
#mostCommon = counter.most_common(50)
#word_names, word_counts = map(list, zip(*mostCommon))
#indexes = np.arange(len(word_names))
#width = 0.7
#plt.bar(indexes, word_counts, width)
#plt.xticks(indexes + width * 0.5, word_names)
#plt.show()
