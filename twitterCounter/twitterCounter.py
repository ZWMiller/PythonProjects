from collections import defaultdict
from bs4 import BeautifulSoup
import string
import requests
import operator
import numpy as np
import matplotlib.pyplot as plt
from twython import Twython
import sys
import wordCountMaker as wcm 
reload(sys)
sys.setdefaultencoding('utf-8')

def get_twitter_app_authorization():
  tup = []
  with open('twitterAuthentication.txt','r') as f:
    for line in f:
      for word in line.strip().split():
        tup.append(word)
  return tup


###################
## Main Program
###################

# Check for correct arguments
try:
  topic = str(sys.argv[1])
  type_select = str(sys.argv[2])
except:
  print "Usage: twitterCounter.py *phrase_to_search* *N/T* (screen name or topic)"
  print "To use #, you must wrap the phrase in ''"
  sys.exit(1)

auth = get_twitter_app_authorization()
twitter = Twython(auth[0], auth[1])

#search for tweets containing a phrase, count the most commonly associated words
topicwords = []
unfiltered_wordlist = []

if type_select == 'T':
  number_of_statuses = 0
  for status in twitter.search(q=topic, count=1000)["statuses"]:
    number_of_statuses+=1
    user = status["user"]["screen_name"].encode('utf-8')
    text = status["text"].encode('utf-8')
    for word in text.strip().split():
      unfiltered_wordlist.append(word)
      if wcm.filter_common_words(word.lower()): 
        continue
      if word.lower() == topic.lower():
        continue
      topicwords.append(wcm.clean_word_for_count(word))
    unfiltered_wordlist.append('<br><br>')
elif type_select == 'N':
  # get the tweets from a user timeline, count the most common words
  user_timeline = twitter.get_user_timeline(screen_name=topic, count=200)
  for tweet in user_timeline:
    user = tweet["user"]["screen_name"].encode('utf-8')
    time = tweet["created_at"].encode('utf-8')
    text = tweet["text"].encode('utf-8')
    for word in text.strip().split():
      unfiltered_wordlist.append(word)
      if wcm.filter_common_words(word.lower()): 
        continue
      topicwords.append(wcm.clean_word_for_count(word))
    unfiltered_wordlist.append('<br><br>')
else:
  print "Type Selection Not Valid."
  print "Usage: twitterCounter.py *phrase_to_search* *N/T* (screen name or topic)"
  print "To use #, you must wrap the phrase in ''"
  sys.exit(1)

dictionary = wcm.make_dictionary_from_wordlist(wordlist)
dictionary_path = 'dictionaries/' + topic + '.txt'
wcm.print_dictionary(dictionary,dictionary_path) # sys prints to temrinal, "filename" prints to file

#make plot from dictionary
page_name =  topic+'.html'
image_name = topic+'.png'
title_name = 'Twitter: ' + topic
wcm.make_word_count_plot(dictionary,image_name,60,title_name)
wcm.make_html_output(page_name,image_name,unfiltered_wordlist,dictionary) 
