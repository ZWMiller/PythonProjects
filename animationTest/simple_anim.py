import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

plt.ion()
fig, ax = plt.subplots()
scat = ax.scatter([],[])
scat.axes.axis([-5, 5, -5, 5])
num_frames = 1000

def update(point):
    array = scat.get_offsets()
    array = np.append(array, point)
    scat.set_offsets(array)
    return scat

def data_gen():
    for _ in range(0,num_frames):
        point = np.random.normal(0, 1, 2)
        yield point

ani = animation.FuncAnimation(fig, update, data_gen, interval=50, blit=False, save_count=num_frames)
ani.save('myanimation.gif',writer='imagemagick',fps=30)
plt.show()
