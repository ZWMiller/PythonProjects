from collections import defaultdict
from bs4 import BeautifulSoup
import string
import requests
import operator
import numpy as np
import matplotlib.pyplot as plt
import sys
import wordCountMaker as wcm
reload(sys)
sys.setdefaultencoding('utf-8')

###################
## Main Program
###################

if __name__ == "__main__":
  # Make the Dictionary with word counts
  wordlist = []
  unfiltered_wordlist=[]
  url = "http://www.gutenberg.org/cache/epub/10/pg10.txt"
  html = requests.get(url).text
  soup = BeautifulSoup(html, 'html5lib')
  text = soup.get_text()
  for word in text.strip().split():
    unfiltered_wordlist.append(word)
    if wcm.filter_common_words(word.lower()): 
      continue
    wordlist.append(wcm.clean_word_for_count(word))
  
  dictionary = defaultdict(int)
  for w in wordlist:
    dictionary[w]+=1

  wcm.print_dictionary(dictionary,'dictionaries/bibleDictionary.txt') #DEBUG
  
  #make plot from dictionary
  page_name = 'bibleIndex.html'
  image_name = 'bibleWordCountPlot.png'
  title_name = 'KJV Bible'
  wcm.make_word_count_plot(dictionary,image_name,60,title_name)
  wcm.make_html_output(page_name,image_name,unfiltered_wordlist,dictionary) 
   
  
  
