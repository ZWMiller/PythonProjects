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

  dictionary = wcm.get_dictionary('bibleDictionary.txt')
  wcm.print_dictionary(dictionary,'bibleDictionary.txt') #DEBUG
  
  #make plot from dictionary
  page_name = 'bibleIndex.html'
  image_name = 'testBibleWordCountPlot.png'
  title_name = 'KJV Bible'
  wcm.make_word_count_plot(dictionary,image_name,60,title_name)
   
  
  
