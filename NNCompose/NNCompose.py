import subprocess
import os
import sys
import numpy as np
import pandas as pd
import random
import csv
# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.utils import np_utils

class midiFile(object):
    def __init__(self,fname):
        self.fname = fname
        self.oname = os.path.splitext(self.fname)[0] + "_NNCompose.mid"
        self.my_cols = ["instrument", "timing", "cmd","pitchshift","note","velocity","timeSig"]
        self.convertMidToCsv()
        self.df = self.convertCsvToDataframe()
        self.header = self.df[self.df['cmd'].str.contains("Header")]
        self.qn = int(self.header.iloc[0]['velocity'])
        self.tempo = int(self.df[self.df['cmd'].str.contains("Tempo")].iloc[0]['pitchshift'])
        self.command = self.df[self.df['instrument'] == 1]
        self.track2 = self.df[self.df['instrument'] == 2]
        self.startTrack = self.track2[self.track2['cmd'].str.contains("Start")]
        self.eof = self.df[self.df['cmd'].str.contains("End_of_file")]
        self.df = self.df[self.df['cmd'].str.contains("Note_on")]
        self.df['note'] = self.df['note'].apply(np.int64)

    def forceDataTypes(self,df):
        df['instrument'] = df['instrument'].astype(int)
        df['timing'] = df['timing'].astype(int)
        df['pitchshift'] = df['pitchshift'].astype(int)
        df['note'] = df['note'].astype(int)
        df['velocity'] = df['velocity'].astype(int)
        df['cmd'] = df['cmd'].astype(str)

    def convertMidToCsv(self):
        basename = os.path.splitext(self.fname)
        inp = "midiIn/" + str(basename[0]) + ".mid"
        out = "csv/" + str(basename[0]) + ".csv"
        cmd = "midicsv " + inp + " >! " + out 
        csvCreated = subprocess.Popen(cmd, shell=True)

    def convertCsvToDataframe(self):
        basename = os.path.splitext(self.fname)
        inp = "csv/" + str(basename[0]) + ".csv"
        return pd.read_csv(inp, names=self.my_cols)

    def convertNotesToName(self):
        notename = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        self.df['noteName'] = self.df['note'].apply(lambda x: int(x % 12))

    def convertMidiToMp3(self):
        basename = os.path.splitext(self.oname)
        inname = "midiOut/" + str(basename[0]) + ".mid"
        outname = "mp3Out/" + str(basename[0]) + ".mp3"
        cmd = "timidity -Ow -o - " + inname + "| lame - " + outname
        mp3Created = subprocess.Popen(cmd, shell=True)

    def makeMidiOut(self,notes):
        basename = os.path.splitext(self.oname)
        filename = "csv/"+str(basename[0])+".csv"
        order = [self.header,self.command,self.startTrack,notes,self.eof]
        with open(filename, 'w') as f:
            for d in order:
                l = d.values.tolist()
                for item in l:
                    outstr = ""
                    if ~np.isnan(item[0]):
                        outstr = outstr + str(int(item[0])) + ", "
                    if ~np.isnan(item[1]):
                        outstr = outstr + str(int(item[1])) + ", " 
                    if item[2]:
                        outstr = outstr + str(item[2].lstrip()) + ", "
                    if ~np.isnan(item[3]):
                        outstr = outstr + str(int(item[3])) + ", "
                    if ~np.isnan(item[4]):
                        outstr = outstr + str(int(item[4])) + ", "
                    if ~np.isnan(item[5]):
                        outstr = outstr + str(int(item[5])) + ", "
                    if item[6]:
                        if ~np.isnan(item[6]):
                            outstr = outstr + str(int(item[6])) + ", "
                    outstr = outstr.rstrip(', ') + "\n"
                    f.write(outstr)
        #outdf.to_csv(filename, sep=" ", header=False, index=False, float_format='%.0f', quoting=3)
        out = "midiOut/" + str(basename[0]) + ".mid"
        cmd = "csvmidi " + filename + " " + out 
        midCreated = subprocess.Popen(cmd, shell=True)

class network(object):
    def __init__(self):
        self.model = self.getModel()

    def getModel(self):
        # create model
        model = Sequential()
        model.add(Dense(12, input_dim=notesToUse, init='uniform', activation='relu'))
        model.add(Dense(10, init='uniform', activation='relu'))
        model.add(Activation('relu'))
        model.add(Dense(8, init='uniform', activation='relu'))
        model.add(Dense(12, init='uniform', activation='softmax'))
        return model

if __name__ == "__main__":
    mf = midiFile("ForestMaze.mid")
    mf.convertNotesToName()
    notes = mf.df['noteName'].values
    
    # split into input (X) and output (Y) variables
    i=0
    notesToUse = 36;
    X = np.empty([int(mf.df.shape[0]),notesToUse],dtype=int)
    Yx = np.empty([int(mf.df.shape[0]),1],dtype=int)
    while i+notesToUse+1 <= notes.size:
        X[i] = notes[i:i+notesToUse]
        Yx[i] = notes[i+notesToUse]
        i+=1

    # one-hot encode output to vector or booleans
    #Y = np_utils.to_categorical(Yx,nb_classes=12)
    
    # fix random seed for reproducibility
    seed = 7
    np.random.seed(seed)
    # Get and Compile model
    NN = network()
    #NN.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # Fit the model
    #NN.model.fit(X, Y, nb_epoch=1, batch_size=20,  verbose=2)
    # calculate predictions
    #predictions = NN.model.predict(X)
    #compare = zip(Y,predictions)
    #for x,y in compare:
    #    print x
    #    print y

    # Generate Notes
    notesToGen = 100
    currentTime = 0
    quarterNote = mf.qn
    notes = []
    for j in range(0,notesToGen):
        #newNote = NN.model.predict(X[0])
        newNote = random.randint(0,11)
        #notes.append([2,currentTime, "Note_on_c", 2, 60+int(newNote.index(max(newNote))), 95])
        notes.append([2,currentTime, "Note_on_c", 2, 60+int(newNote), 95, False])
        beatLength = 3
        while beatLength == 3:
            beatLength = random.randint(1,4)
        dt = int(quarterNote/beatLength)
        currentTime = currentTime+dt
        notes.append([2,currentTime, "Note_off_c", 2, 60+int(newNote), 95, False])
    notes.append([2, currentTime, "End_track"])
    mf.makeMidiOut(pd.DataFrame(notes))
    mf.convertMidiToMp3()
