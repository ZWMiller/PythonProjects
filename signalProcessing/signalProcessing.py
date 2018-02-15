from numpy import *
from matplotlib.mlab import specgram
import matplotlib.pyplot as plt
from scipy.io import wavfile
import seaborn as sns
plt.style.use('seaborn-poster')

class wavFile(object):
    def __init__(self,filename):
        self.data = wavfile.read(filename)[1]
        self.fft()

    def fft(self):
        self.dfft = abs(fft.rfft(self.data))
        self.dfft = 10*log10(self.dfft)

    def plot(self,d,fname,title=None,xname=None,yname=None):
        outname = "img/" + fname 
        plt.clf()
        plt.plot(d)
        plt.title(title)
        plt.xlabel(xname)
        plt.ylabel(yname)
        plt.savefig(outname)

    def plotSpec(self,d,fname,title=None,xname=None,yname=None):
        outname = "img/" + fname 
        plt.clf()
        plt.specgram(d, NFFT=1024, Fs=2, noverlap=900) 
        plt.title(title)
        plt.xlabel(xname)
        plt.ylabel(yname)
        ax = plt.gca()
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)
        plt.savefig(outname)
        ax.yaxis.grid(True)
        ax.xaxis.grid(True)

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
    wv.plot(wv.data[0:500],"sample.png",title="Raw WAV",xname="Time",yname="Signal Strength")
    wv.plot(wv.dfft,"sampleFFT.png",title="Fast Fourier Transform",xname="Frequency",yname="Strength")
    wv.plotSpec(wv.data,"sampleSpec.png",title="Spectrogram",xname="Time",yname="Frequency")
    wv.saveWav("sample.wav")
    
    
