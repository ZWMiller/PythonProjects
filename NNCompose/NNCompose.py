import subprocess
import os
import sys
import numpy as np
import pandas as pd
# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils

class midiFile(object):
    def __init__(self,fname):
        self.fname = fname
        self.convertMidToCsv()
        self.df = self.convertCsvToDataframe()
        self.df = self.df[self.df['cmd'].str.contains("Note_on")]
        self.df['note'] = self.df['note'].apply(np.int64)

    def convertMidToCsv(self):
        basename = os.path.splitext(self.fname)
        inp = "midiIn/" + str(basename[0]) + ".mid"
        out = "csv/" + str(basename[0]) + ".csv"
        cmd = "midicsv " + inp + " >! " + out 
        csvCreated = subprocess.Popen(cmd, shell=True)

    def convertCsvToDataframe(self):
        basename = os.path.splitext(self.fname)
        my_cols = ["instrument", "timing", "cmd","pitchshift","note","velocity"]
        inp = "csv/" + str(basename[0]) + ".csv"
        return pd.read_csv(inp, names=my_cols)

    def convertNotesToName(self):
        notename = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        self.df['noteName'] = self.df['note'].apply(lambda x: int(x % 12))

if __name__ == "__main__":
    mf = midiFile("ForestMaze.mid")
    mf.convertNotesToName()
    notes = mf.df['noteName'].values
    #print notes
    
    # split into input (X) and output (Y) variables
    i=0
    notesToUse = 2;
    X = np.empty([int(mf.df.shape[0]),notesToUse],dtype=int)
    Y = np.empty([int(mf.df.shape[0]),1],dtype=int)
    while i+notesToUse+1 <= notes.size:
        X[i] = notes[i:i+notesToUse]
        Y[i] = notes[i+notesToUse]
        #print X[i], Y[i]
        i+=1

    # one-hot encode output to vector or booleans
    Y = np_utils.to_categorical(Y,nb_classes=12)
    
    # fix random seed for reproducibility
    seed = 7
    np.random.seed(seed)
    # create model
    model = Sequential()
    model.add(Dense(12, input_dim=notesToUse, init='uniform', activation='relu'))
    model.add(Dense(10, init='uniform', activation='relu'))
    model.add(Dense(8, init='uniform', activation='relu'))
    model.add(Dense(12, init='uniform', activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    model.fit(X, Y, nb_epoch=150, batch_size=10,  verbose=2)
    # calculate predictions
    predictions = model.predict(X)
    compare = zip(Y,predictions)
    for x,y in compare:
        print x
        print y
        


