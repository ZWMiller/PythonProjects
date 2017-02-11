from PIL import Image
import sys
import numpy as np
import random
import os 
from sklearn.cluster import KMeans

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

print "Finding Clusters..."
estimator = KMeans(n_clusters=k, n_init=10, init='k-means++')
clusters = estimator.fit_predict(data)
means = estimator.cluster_centers_

print "Preparing image for output..."
numpx = len(data)
for i, clst in enumerate(clusters):
    if not i%10000:
        print "Processing pixel " + str(i) + " / " + str(numpx) + "..."  
    data[i] = map(int, means[clst])

dataOut = [tuple(d) for d in data]

im2 = Image.new(mode,size)
im2.putdata(dataOut)
outname = basename+"_sklreduced.png"
print "Writing out image to " + outname
im2.save(outname)
print "Done!"
