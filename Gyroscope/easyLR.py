import pandas as pd
import numpy as np
from numpy import linalg

# MPU6050
gro = pd.read_csv("MPU6050_filtered.csv")

av = list(gro['Angular velocity'])
ax = list(gro['Axis'])
h = []
for i in range(len(ax)):
    if ax[i] == 'X':
        h.extend([av[i], 0, 0])
    elif ax[i] == 'Y':
        h.extend([0, av[i], 0])
    elif ax[i] == 'Z':
        h.extend([0, 0, av[i]])
h = np.reshape(h, (len(ax), 3))

x, y, z = gro['X'], gro['Y'], gro['Z']
x = list(x)
x = np.reshape(x, (len(x), 1))
y = list(y)
y = np.reshape(y, (len(y), 1))
z = list(z)
z = np.reshape(z, (len(z), 1))
H = np.hstack([x, y, z, np.ones((len(x), 1))])

print(linalg.lstsq(H, h, rcond=None)[0])
