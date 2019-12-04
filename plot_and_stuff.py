
import numpy as np
import time
import matplotlib.pyplot as plt
plt.close('all')
# draw the figure so the animations will work
fig = plt.gcf()
fig.show()
fig.canvas.draw()

# plt.close(fig)

while True:
    # compute something

    x = np.random.randint(0, 50)
    y = np.random.randint(0, 50)
    plt.plot([x], [y], 'r+')
    # update canvas immediately
    plt.xlim([0, 100])
    plt.ylim([0, 100])
    # plt.pause(0.01)  # I ain't needed!!!
    fig.canvas.draw()
