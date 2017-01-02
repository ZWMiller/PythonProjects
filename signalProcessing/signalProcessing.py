from numpy import *
from pylab import specgram
import matplotlib.pyplot as plt
from scipy.io import wavfile

class wavFile(object):
    def __init__(self,filename):
        self.data = wavfile.read(filename)[1]
        self.fft()

    def fft(self):
        self.dfft = abs(fft.rfft(self.data))
        self.dfft = 10*log10(self.dfft)

    def plot(self,d,fname):
        outname = "img/" + fname 
        plt.clf()
        plt.plot(d)
        plt.savefig(outname)

    def plotSpec(self,d,fname):
        outname = "img/" + fname 
        plt.clf()
        sg = specgram(d)
        plt.savefig(outname)

    def saveWav(self,fname):
        outname = "output/" + fname 
        wavfile.write(outname,44100,self.data)

if __name__ == "__main__":
    # Generate a signal 
    smplrate = 10000.
    inp = arange(10000,dtype=int16)
    sin1 = 20000*sin(2*pi*(440./smplrate)*inp)
    sin2 = 20000*sin(2*pi*(1000./smplrate)*inp)
    signal = sin1+sin2
    wavfile.write("input/sample.wav",44100,signal)
    
    wv = wavFile("input/sample.wav")
    wv.plot(wv.data,"sample.png")
    wv.plot(wv.dfft,"sampleFFT.png")
    wv.plotSpec(wv.data,"sampleSpec.png")
    wv.saveWav("sample.wav")
    
    
