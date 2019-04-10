import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

euler = pd.read_csv("EULER.csv")
mag = pd.read_csv("MAG.csv")
sun = pd.read_csv("SUN.csv")

euraw, eukal = euler['raw'], euler['kal']
magx, magy = mag['x'], mag['y']
sunx, suny = sun['x'], sun['y']

plt.figure()
plt.plot(euraw[1200:1300], label="raw")
plt.plot(eukal[1200:1300], label="kal")
plt.title("Local")
plt.xlabel("data points")
plt.ylabel("Angle / °")
plt.legend()

plt.figure()
plt.plot(euraw, label="raw")
plt.plot(eukal, label="kal")
plt.title("Overview")
plt.xlabel("data points")
plt.ylabel("Angle / °")
plt.legend()

plt.figure()
plt.plot(euraw[211:318], label="raw")
plt.plot(eukal[211:318], label="kal")
plt.title("Local")
plt.xlabel("data points")
plt.ylabel("Angle / °")
plt.legend()

div = [5, 77, 120, 177, 211, 318, 376, 485, 546, 661, 730, 860, 1085, 1208, 1263, 1337, 1386, 1446,
       1496, 1567, 1628, 1720, 1794, 1868]

i = 0
raw = 0
kal = 0
point = 0
while i < len(div)-1:
    point = point + div[i+1]-div[i] + 1
    raw = raw + np.var(euraw[div[i]:div[i+1]])*(div[i+1]-div[i] + 1)
    kal = kal + np.var(eukal[div[i]:div[i+1]])*(div[i+1]-div[i] + 1)
    i = i + 2

print(raw / point)
print(kal/point)


# plt.figure()
# plt.plot(eukal)

plt.show()

