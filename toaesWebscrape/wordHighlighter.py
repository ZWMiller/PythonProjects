from collections import Counter
from collections import defaultdict
from bs4 import BeautifulSoup
import requests
import operator
from pprint import pprint
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def clean_word_for_count(w): 
  w.replace(',','')
  w.replace('.','')
  w.replace('\'','')
  return w.lower()

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

def get_max_counts_in_dictionary(dictionary):
  for w in sorted(dictionary, key=dictionary.get, reverse=True):
    return dictionary[w]

def get_word_count_ratio(word, dictionary):
  return float(float(dictionary[word])/float(get_max_counts_in_dictionary(dictionary)))

def get_word_color(word,dictionary):
  r = get_word_count_ratio(word,dictionary)
  return get_color(r)
 
def get_color(r):
  if r > 0.9:
    return '#ff0000'
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

# Make the Dictionary with word counts
wordlist = []
unfiltered_wordlist=[]
for i in range(1,12):
  url = "http://toaes.kyletolle.com/v4/ch" + str(i) + "/"
  html = requests.get(url).text
  soup = BeautifulSoup(html, 'html5lib')
  text = soup.get_text()
  #print text
  for word in text.strip().split():
    unfiltered_wordlist.append(word)
    if filter_common_words(word.lower()): 
      continue
    wordlist.append(clean_word_for_count(word))

dictionary = defaultdict(int)
sorted_dictionary = defaultdict(int)
for w in wordlist:
  dictionary[w]+=1
#for w in sorted(dictionary, key=dictionary.get, reverse=True):
#   print w + " " + str(dictionary[w]) + " " + str(get_word_count_ratio(w, dictionary))

# make an html page that colors each word according to it's frequency
with open('index.html', 'w') as file:
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



