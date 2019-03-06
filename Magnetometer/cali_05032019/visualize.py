import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import linalg
import scipy
from scipy.optimize import lsq_linear

mag = pd.read_csv("emg.csv")

plt.figure(1)
x, y, z = mag['x'][100:-100], mag['y'][100:-100], mag['z'][100:-100]

# ax = plt.subplot(111, projection='3d')
# plt.title("External magnetometer")
# ax.scatter(x, y, z, c='b')
# ax.set_zlabel('Z')
# ax.set_ylabel('Y')
# ax.set_xlabel('X')

# plt.figure(2)
# plt.plot(x, y, 'ro')
# plt.title("x-y Plane")
# plt.xlabel("x / mG")
# plt.ylabel("y / mG")
#
# plt.figure(3)
# plt.plot(x, z, 'go')
# plt.title("x-z Plane")
# plt.xlabel("x / mG")
# plt.ylabel("z / mG")
#
# plt.figure(4)
# plt.plot(y, z, 'bo')
# plt.title("y-z Plane")
# plt.xlabel("y / mG")
# plt.ylabel("z / mG")
#
# plt.show()

x = list(x)
y = list(y)
z = list(z)

length = len(x)

x = np.array(x).reshape(length, 1)
y = np.array(y).reshape(length, 1)
z = np.array(z).reshape(length, 1)

H = np.hstack((x, y, z, -y ** 2, -z ** 2, np.ones([length, 1])))
w = np.square(x)

print(H.shape)
print(w.shape)

(X, residues, rank, shape) = linalg.lstsq(H, w, rcond=None)

OSx = X[0] / 2
OSy = X[1] / (2 * X[3])
OSz = X[2] / (2 * X[4])

A = X[5] + OSx ** 2 + X[3] * OSy ** 2 + X[4] * OSz ** 2
B = A / X[3]
C = A / X[4]

SCx = np.sqrt(A)
SCy = np.sqrt(B)
SCz = np.sqrt(C)

print([OSx, OSy, OSz, SCx, SCy, SCz])