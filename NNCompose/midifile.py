import subprocess
import os
import sys
import numpy as np
import pandas as pd
import random
import csv
import time
from operator import itemgetter

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
        if not os.path.isfile(inp):
            print("Did not find .mid file, trying .midi!")
            inp = "midiIn/" + str(basename[0]) + ".midi"
            if not os.path.isfile(inp):
                raise ValueError("No MIDI File Found")
        out = "csv/" + str(basename[0]) + ".csv"
        cmd = "midicsv " + inp + " >! " + out 
        csvCreated = subprocess.Popen(cmd, shell=True)
        print("Converting to CSV")
        time.sleep(5)

    def convertCsvToDataframe(self):
        basename = os.path.splitext(self.fname)
        inp = "csv/" + str(basename[0]) + ".csv"
        return pd.read_csv(inp, names=self.my_cols)

    def convertNotesToName(self):
        notename = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        #self.df['noteName'] = self.df['note'].apply(lambda x: int(x % 12))
        self.df['noteName'] = self.df['note'] #if trying to include octaves)

    def convertMidiToMp3(self):
        basename = os.path.splitext(self.oname)
        inname = "midiOut/" + str(basename[0]) + ".mid"
        outname = "mp3Out/" + str(basename[0]) + ".mp3"
        cmd = "timidity -Ow -o - " + inname + "| lame - " + outname
        mp3Created = subprocess.Popen(cmd, shell=True)
        time.sleep(5)
        print("Created ", outname)
        
    def get_trainable_arrays(self, seq_length=10):
        data = self.df['note'].values
        x = []
        y = []
        for i in range(seq_length,len(data)):
            x.append(data[i-seq_length:i])
            y.append(data[i])
        print("X & Y Correlation:\n",x[0],y[0],"\nActual Data Correlation:\n",data[seq_length-2:seq_length+1])
        X = np.reshape(x, (len(x), seq_length, 1))
        Y = np.reshape(y, len(y))
        return X,Y
        
    def encode_target(self, y):
        n_values = 128
        ohe = np.eye(n_values)[y]
        return ohe
    
    def convert_to_midi_format(self, result_notes):
        notes = []
        currentTime = 0

        for ind in result_notes:
            beatLength = 3
            while beatLength in [3,5,6,7]:
                beatLength = random.randint(1,4)
            dt = int(self.qn/beatLength)
            endtime = currentTime + dt
            
            for note in ind:
                notes.append([2,currentTime, "Note_on_c", 2, int(note), 95,False])
                notes.append([2,endtime, "Note_off_c", 2, int(note), 95, False])
            currentTime = endtime
        notes.append([2, currentTime, "End_track"])
        return sorted(notes,key=itemgetter(1))
    
    def check_valid_entry(self, item):
        if type(item) == str:
            return True
        elif not np.isnan(item):
            return True
        else:
            return False    

    def makeMidiOut(self,notes):
        basename = os.path.splitext(self.oname)
        filename = "csv/"+str(basename[0])+".csv"
        file_order = [self.header,self.command,self.startTrack,notes]
        with open(filename, 'w') as f:
            for section in file_order:
                if not type(section) == list:
                    try:
                        l = section.values.tolist()
                    except AttributeError:
                        l = section.tolist()
                else:
                    l = section
                for item in l:
                    outstr = ""
                    
                    if len(item) == 3:
                        if self.check_valid_entry(item[0]):
                            outstr = outstr + str(int(item[0])) + ", "
                        if self.check_valid_entry(item[1]):
                            outstr = outstr + str(int(item[1])) + ", " 
                        if self.check_valid_entry(item[2]):
                            outstr = outstr + str(item[2].lstrip(' ')) + ", "
                    else:
                        if self.check_valid_entry(item[0]):
                            outstr = outstr + str(int(item[0])) + ", "
                        if self.check_valid_entry(item[1]):
                            outstr = outstr + str(int(item[1])) + ", " 
                        if self.check_valid_entry(item[2]):
                            outstr = outstr + str(item[2].lstrip(' ')) + ", "
                        if self.check_valid_entry(item[3]):
                            if type(item[3]) == str:
                                outstr = outstr + str(item[3]) + ", "
                            else:
                                outstr = outstr + str(int(item[3])) + ", "
                        if self.check_valid_entry(item[4]):
                            outstr = outstr + str(int(item[4])) + ", "
                        if self.check_valid_entry(item[5]):
                            outstr = outstr + str(int(item[5])) + ", "
                        if self.check_valid_entry(item[6]):
                            outstr = outstr + str(int(item[6])) + ", "
                    outstr = outstr.rstrip(', ') + "\n"
                    f.write(outstr)
            item = self.eof.iloc[0].values
            if self.check_valid_entry(item[0]):
                outstr = outstr + str(int(item[0])) + ", "
            if self.check_valid_entry(item[1]):
                outstr = outstr + str(int(item[1])) + ", " 
            if self.check_valid_entry(item[2]):
                outstr = outstr + str(item[2].lstrip(' ')) + ", "
            outstr = outstr.rstrip(', ') + "\n"
            f.write(outstr)
        self.csv_to_midi()
    
    def csv_to_midi(self):
        basename = os.path.splitext(self.oname)
        filename = "csv/"+str(basename[0])+".csv"
        out = "midiOut/" + str(basename[0]) + ".mid"
        cmd = "csvmidi " + filename + " " + out 
        midCreated = subprocess.Popen(cmd, shell=True)
        print("Converting to MIDI")
        time.sleep(5)