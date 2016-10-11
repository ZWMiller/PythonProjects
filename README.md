# Learning Python

These will be my forays into learning Python for data science. I'll track my
projects here with a quick note on what each project does.

##Twitter Counter

This code connects to the Twitter API and searches for tweets based on a
keyword provided by the user. It then gets the text of the tweets and counts
all the words (filtering the most common words like "of" or "the") and prints
a word count for the N most common words in tweets that match the search.
There is also an example of using the Twitter API to look up a users stream
and then search through their tweets to get their most commonly used words.

## TOAES Webscrape

This code loads a webpage that contains a tale my friend is working on. It
finds the text of the book and then deconstructs that into a series of words
and once again counts the occurences of each word. This was designed to reuse
much of the idea from the Twitter Counter, but apply it to data picked out of
a webpage using the BeautifulSoup Library.
