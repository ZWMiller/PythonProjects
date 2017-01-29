import numpy as np
import matplotlib.pyplot as plt

#plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
hl, = ax.plot(np.arange(10000),np.random.randn(10000))
plt.pause(0.1)

def update():
    hl.set_xdata(np.arange(10000))
    hl.set_ydata(np.random.randn(10000))
    plt.pause(0.1)

while True:
    print "i"
    update()



