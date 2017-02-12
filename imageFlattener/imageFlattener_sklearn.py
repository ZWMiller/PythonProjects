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
    while width > 2000 and height > 2000:
        print "Image too large, downsizing by factor of 2..."
        image = image.resize((int(width/2),int(height/2)),Image.ANTIALIAS)
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
numpx = len(data)
print "Checking for sanity..."
if k > len([list(x) for x in set(tuple(x) for x in data)]):
    print "Fewer colors than clusters"
    sys.exit(1)

print "Finding " + str(k) + " color clusters and appropriate replacement colors..."
print "(This can take a while. Your image has " + str(numpx) + " pixels to analyze."
print "The length of time depends on number of pixels, number of colors in"
print "image and the number of requested output colors. Please be patient.)"
estimator = KMeans(n_clusters=k, n_init=10, init='k-means++')
clusters = estimator.fit_predict(data)
means = estimator.cluster_centers_

print "Preparing image for output..."
for i, clst in enumerate(clusters):
    if not i%100000 and numpx > 100000:
        print "Processing pixel " + str(i) + " / " + str(numpx) + "..."  
    elif not i%100000:
        print "Processing pixels."
    data[i] = map(int, means[clst])

dataOut = [tuple(d) for d in data]

im2 = Image.new(mode,size)
im2.putdata(dataOut)
outname = basename+"_sklreduced_"+str(k)+"clusters.png"
print "Writing out image to " + outname
im2.save(outname, quality=85, optimize=True)
print "Done!"
