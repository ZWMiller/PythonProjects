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
  for i in range(1,12):
    url = "http://toaes.kyletolle.com/v4/ch" + str(i) + "/"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')
    for x in soup.findAll("p"):
      if wcm.is_title_text(x.text):
        continue
      for word in x.text.strip().split():
        unfiltered_wordlist.append(word)
        if wcm.filter_common_words(word.lower()): 
          continue
        wordlist.append(wcm.clean_word_for_count(word))
    unfiltered_wordlist.append('<br><br>')
  
  dictionary = defaultdict(int)
  for w in wordlist:
    dictionary[w]+=1

  wcm.print_dictionary(dictionary,'toaesDictionary.txt') # sys prints to temrinal, "filename" prints to file
  
  #make plot from dictionary
  page_name = 'toaesIndex.html'
  image_name = 'toaesWordCountPlot.png'
  title_name = 'ToaES v4'
  wcm.make_word_count_plot(dictionary,60,image_name,title_name)
  wcm.make_html_output(page_name,image_name,unfiltered_wordlist,dictionary) 
   
  
  
