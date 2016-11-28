from operator import itemgetter

HOF = [["steve",0.12],["doug",0.35],["mike",0.27],["reg",0.95],["peter",1.0],["evan",0.01]]

sortHOF=sorted(HOF, reverse=True, key=itemgetter(1))

print sortHOF
