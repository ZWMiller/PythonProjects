from collections import Counter
from bs4 import BeautifulSoup
import requests

def clean_word_for_count(w): 
  w.replace(',','')
  w.replace('.','')
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

wordlist = []

for i in range(1,12):
  print i
  url = "http://toaes.kyletolle.com/v4/ch" + str(i) + "/"
  html = requests.get(url).text
  soup = BeautifulSoup(html, 'html5lib')
  text = soup.get_text()
  #print text
  for word in text.strip().split():
    if filter_common_words(word.lower()): 
      continue
    wordlist.append(clean_word_for_count(word))

print "\n@kyletolle's most used words: "
counter = Counter(wordlist)
print_counter_words(counter,100)
