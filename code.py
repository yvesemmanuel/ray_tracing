import numpy as np
import matplotlib.pyplot as plt

width = 300
height = 200

camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio) # left, top, right, bottom

image = np.zeros((height, width, 3))

plt.imsave('image.png', image)