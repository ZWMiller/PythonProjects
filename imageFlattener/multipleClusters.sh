#!/bin/bash

if [ $# -ne 3 ]; then
    echo "Usage: ./multipleClusters.sh imageName.png startNum endNum"
fi
filename=$1
k=$2
end=$3

while [ "$k" -le "$end" ]; do
  echo "Working on $k clusters version..."
  python imageFlattener_sklearn.py $filename $k
  k=$(($k + 1))
done
