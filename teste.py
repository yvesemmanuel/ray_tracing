import numpy as np


a = np.array([1, 0, 1])
b = np.array([-2, 2, -2])

Tca = np.dot(a, b)
D_sqrt = np.dot(a, a) - (Tca ** 2)

image = np.zeros((2, 2, 3))

print(image[0][0])