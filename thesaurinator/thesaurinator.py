import sys
from nltk.corpus import wordnet as wn
import random

raw = str(sys.stdin.readlines())

out = []
for word in raw.lower().split():
    syns = []
    for ss in wn.synsets(word):
        for s in ss.lemma_names():
            syns.append(s)
    if len(syns) > 0:
        out.append(random.choice(syns))
    else:
        out.append(word)

print(' '.join(out))

