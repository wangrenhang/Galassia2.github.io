import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

OSx, OSy, OSz, SCx, SCy, SCz = [-46.9397, 11.1385, 53.3092, 0.8583, 0.8132, 0.7972]

# RM3100
mag = pd.read_csv("emg.csv")
# Milligauss meter
mgm = pd.read_csv("mgm.csv")

# Internal magneto
img = pd.read_csv("img.csv")
img_old = pd.read_csv("img_old.csv")

# 3-D HMC5843 test1
plt.figure(6)
x, y, z = img['x'], img['y'], img['z']
ax = plt.subplot(111, projection='3d')
plt.title("HMC5843 test1")
ax.scatter(x, y, z, c='b')
ax.set_zlabel('Z')
ax.set_ylabel('Y')
ax.set_xlabel('X')

# 3-D HMC5843 test2
plt.figure(7)
x, y, z = img_old['x'], img_old['y'], img_old['z']
ax = plt.subplot(111, projection='3d')
plt.title("HMC5843 test2")
ax.scatter(x, y, z, c='b')
ax.set_zlabel('Z')
ax.set_ylabel('Y')
ax.set_xlabel('X')

# 3-D Milligauss meter
plt.figure(1)
x, y, z = mgm['x'], mgm['y'], mgm['z']
ax = plt.subplot(111, projection='3d')
plt.title("Milligauss meter")
ax.scatter(x, y, z, c='b')
ax.set_zlabel('Z')
ax.set_ylabel('Y')
ax.set_xlabel('X')

#  3-D RM3100
plt.figure(2)
x, y, z = mag['x'][100:-100], mag['y'][100:-100], mag['z'][100:-100]
ax = plt.subplot(111, projection='3d')
plt.title("RM3100")
ax.scatter(x, y, z, c='b')
ax.set_zlabel('Z')
ax.set_ylabel('Y')
ax.set_xlabel('X')

#  3-D Calibrated RM3100
plt.figure(8)
xc = (x - OSx) * SCx
yc = (y - OSy) * SCy
zc = (z - OSz) * SCz
ax = plt.subplot(111, projection='3d')
plt.title("Calibrated RM3100")
ax.scatter(xc, yc, zc, c='b')
ax.set_zlabel('Z')
ax.set_ylabel('Y')
ax.set_xlabel('X')

plt.figure(3)
plt.plot(x, y, 'ro')
plt.title("x-y Plane")
plt.xlabel("x / mG")
plt.ylabel("y / mG")

plt.figure(4)
plt.plot(x, z, 'go')
plt.title("x-z Plane")
plt.xlabel("x / mG")
plt.ylabel("z / mG")

plt.figure(5)
plt.plot(y, z, 'bo')
plt.title("y-z Plane")
plt.xlabel("y / mG")
plt.ylabel("z / mG")

plt.show()