import pandas as pd
import numpy as np
from numpy import linalg

# RM3100
mag = pd.read_csv("emg.csv")
# Milligauss meter
mgm = pd.read_csv("mgm.csv")

# Get href from Milligauss meter
href = mgm['h']
href = np.mean(href)

# Filter bad points
x, y, z = mag['x'][100:-100], mag['y'][100:-100], mag['z'][100:-100]

x = list(x)
y = list(y)
z = list(z)

length = len(x)

x = np.array(x).reshape(length, 1)
y = np.array(y).reshape(length, 1)
z = np.array(z).reshape(length, 1)

H = np.hstack((x, y, z, -y ** 2, -z ** 2, np.ones([length, 1])))
w = np.square(x)

(X, residues, rank, shape) = linalg.lstsq(H, w, rcond=None)
print(residues)

# Offsets
OSx = X[0] / 2
OSy = X[1] / (2 * X[3])
OSz = X[2] / (2 * X[4])

A = X[5] + OSx ** 2 + X[3] * OSy ** 2 + X[4] * OSz ** 2
B = A / X[3]
C = A / X[4]

# Scales
SCx = href / np.sqrt(A)
SCy = href / np.sqrt(B)
SCz = href / np.sqrt(C)

print([OSx[0], OSy[0], OSz[0], SCx[0], SCy[0], SCz[0]])