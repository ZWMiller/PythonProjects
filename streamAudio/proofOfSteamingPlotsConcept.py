import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#plt.ion()
f,ax = plt.subplots(2)
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-2,2)
ax[0].set_title("Raw Audio Signal")
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,5000)
ax[1].set_ylim(-100,100)
ax[1].set_title("Fast Fourier Transform")
plt.pause(0.01)
plt.tight_layout()
def update():
    audio_data = np.random.randn(10000)
    dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)
    plt.pause(0.1)

while True:
    update()



