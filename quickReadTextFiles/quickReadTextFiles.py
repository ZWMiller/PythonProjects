import csv

totalLumi = 0.
files = ["470904.txt","470914.txt","480904.txt","490904.txt"]

for fileName in files:
    trigLumi = 0.
    with open(fileName,'r') as f:
        for line in f:
            run, date, ploty, lumi, ps = line.split()
            trigLumi += float(lumi)
            totalLumi += float(lumi)
    print fileName + " " + str(trigLumi) 

print totalLumi
