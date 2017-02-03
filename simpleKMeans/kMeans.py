import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import random

k = 3
saveImg = True

class cluster(object):
    def __init__(self):
        self.mean = None
        self.members = []
        self.prevMembers = []
        self.color = next(colors)

    def setPrevMembers(self):
        self.prevMembers = self.members

    def addMember(self,pt):
        self.members.append(pt)
    
    def isChanged(self):
        return self.members != self.prevMembers

    def getMean(self):
        if not len(self.members):
            self.mean = [-999,-999]
            return
        x,y = 0.,0.
        for p in self.members:
            x+=p[0]
            y+=p[1]
        self.mean = [x/len(self.members),y/len(self.members)]

    def getTotalSquareDistance(self):
        val = 0.
        for p in self.members:
            val += computeDistance(self,p)**2
        return val

def computeDistance(clst, pt):
    return np.sqrt((pt[0] - clst.mean[0])**2 + (pt[1] - clst.mean[1])**2)

def classify(clusters,pt):
    return min(range(k), key=lambda i: computeDistance(clusters[i],p))

def plotClusters(clusters, i):
    plt.clf()
    for c in clusters:
        if not c.members:
            continue
        x,y = zip(*c.members)
        mx,my = c.mean
        plt.scatter(x, y, color=c.color)
        plt.scatter(mx,my, color='b', marker='x', s=400)
    if saveImg:
        plt.savefig('kmeans_'+str(i)+'Clusters.png')
    #plt.pause(0.2)

# Generate data to test on
np.random.seed(9)
data = []
for i in range(0,k):
    for _ in range(0,100):
        data.append([np.random.normal(4*i),np.random.normal(i)])
x1,y1 = zip(*data)
plt.xlabel('X')
plt.ylabel('Y')
plt.scatter(x1,y1)
plt.savefig('kmeansStep_Init.png')
#plt.pause(0.2)

k=1
findKPoints = []
while k<=9:
    #initialize clusters
    colors = iter(cm.rainbow(np.linspace(0, 1, 10)))
    clusters = [cluster() for _ in range(0,k)]
    for c in clusters:
        c.mean = random.choice(data)
        
    for p in data:
        clusterNum = classify(clusters,p)
        clusters[clusterNum].addMember(p)
    
    #plotClusters(clusters,0)
    
    # Minimize!
    ischange = True
    i = 1
    while ischange and i < 1000:
        ischange = False
    
        for c in clusters:
            c.getMean()
            c.setPrevMembers()
            c.members = []
        
        for p in data:
            clusterNum = classify(clusters,p)
            clusters[clusterNum].addMember(p)
    
        #plotClusters(clusters,i)
        for c in clusters:
            if c.isChanged():
                ischange = True
        i += 1 
    
    # make the plots
    plotClusters(clusters,k)
    totalSquareDistance = 0.
    for c in clusters:
        totalSquareDistance += c.getTotalSquareDistance()
    findKPoints.append([k,totalSquareDistance])
    k+=1
x,y = zip(*findKPoints)
plt.clf()
plt.xlabel('Number of Clusters')
plt.ylabel('Sum of Squared Distance To Mean')
plt.plot(x,y)
plt.savefig('kmeans_findK.png')
#plt.show()
                                
