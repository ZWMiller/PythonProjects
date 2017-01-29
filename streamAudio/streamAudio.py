import pyaudio
import numpy as np
import pylab
import matplotlib.pyplot as plt
from scipy.io import wavfile
import time
import sys

p = pyaudio.PyAudio()
i=0
fig = plt.figure()
ax = fig.add_subplot(111)

# some X and Y data
x = np.arange(2000)
y = np.random.randn(2000)
li, = ax.plot(x, y)
ax.set_xlim(0,1000)
ax.set_ylim(-2,2)
plt.pause(0.2)

def callback(in_data, frame_count, time_info, flag):
    global i
    audio_data = np.fromstring(in_data, dtype=np.float32)
    #dfft = 10*np.log10(abs(np.fft.rfft(audio_data)))
    plotvar = audio_data
    li.set_xdata(np.arange(len(plotvar)))
    li.set_ydata(plotvar)
    plt.pause(0.2)
    time.sleep(0.2)
    return (audio_data, pyaudio.paContinue)

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=False,
                input=True,
                stream_callback=callback)

stream.start_stream()
print "Press Ctrl+C to Break Recording"
while stream.is_active():
    try:
        i=1
    except KeyboardInterrupt:
        break

stream.stop_stream()
stream.close()

p.terminate()
