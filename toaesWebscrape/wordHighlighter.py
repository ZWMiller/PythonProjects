from collections import defaultdict
from bs4 import BeautifulSoup
import string
import requests
import operator
import numpy as np
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def clean_word_for_count(w): 
  wr = "".join(l for l in w if l not in string.punctuation)
  return wr.lower()

def filter_common_words(w):
  common_words = ['a', 'the', 'an', 'to', 'i', 'and', 'for', 'of', 'is', 'in', 'that', 'it', 'on', 'you',
      'with','are','my','if','at','as','by','was','be','but','were','had']
  if w in common_words:
    return True
  else:
    return False

def get_max_counts_in_dictionary(dictionary):
  for w in sorted(dictionary, key=dictionary.get, reverse=True):
    return dictionary[w]

def print_dictionary(dictionary):
  for w in sorted(dictionary, key=dictionary.get, reverse=True):
    print w + " " + str(dictionary[w])

def get_word_count_ratio(word, dictionary):
  return float(float(dictionary[word])/float(get_max_counts_in_dictionary(dictionary)))

def is_title_text(text):
  if text == "Thoughts of An Eaten Sun > v4":
    return True
  else:
    return False

def get_word_color(word,dictionary):
  r = get_word_count_ratio(word,dictionary)
  return get_color(r)
 
def get_color(r):
  if r > 0.9:
    return 'ff0000'
  elif r > 0.8:
    return 'ff6600'
  elif r > 0.7:
    return 'ffff00'
  elif r > 0.6:
    return '99ff33'
  elif r > 0.5:
    return '66ffcc'
  elif r > 0.4:
    return '00ccff'
  elif r > 0.3:
    return 'ff6600'
  elif r > 0.2:
    return '0066ff'
  elif r > 0.1:
    return '6600cc'
  else:
    return '000000'

def make_word_count_plot(dictionary):
  index=0
  limit=100
  x = list()
  y = list()
  colors = list()
  for w in sorted(dictionary, key=dictionary.get, reverse=True):
    x.append(w)
    y.append(dictionary[w])
    colors.append('#'+get_word_color(clean_word_for_count(w),dictionary))
    index+=1
    if index >= limit: 
      break
  fig, ax = plt.subplots()
  bar_width = 0.35
  opacity = 0.4
  index2 = np.arange(limit)
  rects1 = plt.bar(index2, y, bar_width, alpha=opacity, color=colors)
  plt.xlabel('Words')
  plt.ylabel('Counts')
  plt.title('{} Most Common Words in Text'.format(str(limit)))
  plt.xticks(index2 + bar_width, x, rotation=90, fontsize=11)
  for ii in reversed(range(0,10)):
    il = float(ii)/10.
    ypos = 0.85 - float(ii)/30.
    ii = ii*10
    colors = '#'+get_color(0.05+il)
    ax.text(0.65,ypos,'Top {}% of Words'.format(ii),color=colors,transform = ax.transAxes)
  plt.show()

def make_html_output(page_name,unfiltered_wordlist,dictionary):
 with open(page_name, 'w') as file:
    line1 = '<html lang="en">'
    line2 = '<head>'
    line3 = '<meta charset="utf-8">'
    line4 = '</head>'
    line5 = '<body>'
    line6 = '<p>'
    file.write('{}\n{}\n{}\n{}\n{}\n{}'.format(line1,line2,line3,line4,line5,line6))
  
    for word in unfiltered_wordlist:
      color = get_word_color(clean_word_for_count(word),dictionary)
      if color == '000000':
        file.write('{} '.format(word))
      else:
        file.write('<font color=#{}><b>{} </b></font>'.format(color,word))
    line1 = '</p>'
    line2 = '</body>'
    line3 = '</html>'
    file.write('\n{}\n{}\n{}'.format(line1,line2,line3))


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
      #print x.text #DEBUG
      if is_title_text(x.text):
        continue
      for word in x.text.strip().split():
        unfiltered_wordlist.append(word)
        if filter_common_words(word.lower()): 
          continue
        wordlist.append(clean_word_for_count(word))
    unfiltered_wordlist.append('<br><br>')
  
  dictionary = defaultdict(int)
  for w in wordlist:
    dictionary[w]+=1

  #print_dictionary(dictionary) #DEBUG
  
  #make plot from dictionary
  make_word_count_plot(dictionary)
  make_html_output('index.html',unfiltered_wordlist,dictionary) 
   
  
  
