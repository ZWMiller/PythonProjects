from PIL import Image
import sys
import numpy as np
import random
import os 

def get_image(image_path):
    print "Loading the image..."
    image = Image.open(image_path, 'r')
    width, height = image.size
    pixel_values = list(image.getdata())
    if image.mode == 'RGB':
        channels = 3
    elif image.mode == 'L':
        channels = 1
    elif image.mode == 'RGBA':
        channels = 3
        for px in pixel_values:
            px = list(px)
            R,G,B,A = px 
            px[0] = ((1-A)*R) + A*R
            px[1] = ((1-A)*G) + A*G
            px[2] = ((1-A)*B) + A*B
            del px[3]
            px = tuple(px)
    else:
        print("Unknown mode: %s" % image.mode)
        return None
    return pixel_values,image.mode,image.size

class cluster(object):
    def __init__(self, i):
        self.mean = None
        self.id = i
        self.members = []
        self.prevMembers = []

    def setPrevMembers(self):
        self.prevMembers = self.members

    def addMember(self,pt):
        self.members.append(pt)
    
    def isChanged(self):
        return self.members != self.prevMembers

    def getMean(self):
        if not len(self.members):
            print "You have a cluster with no members, idiot"
            print " - it has mean " + str(self.mean)
            self.mean = [-999,-999,-999]
            return
        x,y,z = 0.,0.,0.
        for p in self.members:
            x+=p[0]
            y+=p[1]
            z+=p[2]
        self.mean = [int(x/len(self.members)),int(y/len(self.members)),int(z/len(self.members))]

    def getTotalSquareDistance(self):
        val = 0.
        for p in self.members:
            val += computeDistance(self,p)**2
        return val

def computeDistance(clst, pt):
    return np.sqrt((pt[0]-clst.mean[0])**2 + (pt[1]-clst.mean[1])**2 + (pt[2]-clst.mean[2])**2)

def classify(clusters,pt):
    return min(range(k), key=lambda i: computeDistance(clusters[i],p))

def processInputs(inp):
    fn, k = inp
    bn = os.path.splitext(fn)[0]
    try:
        k = int(k)
        if k <= 0:
            print "Invalid Cluster Number, Default to 2"
            k=2
        else:
            k = int(k)
    except:
        "Cluster value NaN; default to 2"
        k=2
    return fn, bn, int(k)

### MAIN ###
if len(sys.argv) != 3:
    print "Usage: imageFlattener.py file.png num_clusters"
    sys.exit(1)
filename, basename, k = processInputs(sys.argv[1:3])

dataTuple,mode,size = get_image(filename)
data = map(list,dataTuple)
print "Checking for sanity..."
if k > len([list(x) for x in set(tuple(x) for x in data)]):
    print "Fewer colors than clusters"
    sys.exit(1)

clusters = [cluster(j) for j in range(0,k)]
means = []
print "Initializing Clusters..."
for c in clusters:
    while True:
        mn = random.choice(data)
        if mn not in means:
            means.append(mn)
            break
    c.mean = mn
        
for p in data:
    clusterNum = classify(clusters,p)
    clusters[clusterNum].addMember(p)


# Minimize!
ischange = True
i = 1
while ischange and i < 1000:
    print "Flattening Image, Iteration: " + str(i)
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

print "Preparing image for output..."
numpx = len(data)
for i, pt in enumerate(data):
    if not i%10000:
        print "Processing pixel " + str(i) + " / " + str(numpx) + "..."  
    for c in clusters:
        if pt in c.members:
            data[i] = c.mean
            break

dataOut = [tuple(d) for d in data]

im2 = Image.new(mode,size)
im2.putdata(dataOut)
outname = basename+"_reduced.png"
print "Writing out image to " + outname
im2.save(outname)
print "Done!"
