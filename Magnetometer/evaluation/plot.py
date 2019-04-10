import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

euler = pd.read_csv("EULER.csv")
mag = pd.read_csv("MAG.csv")
sun = pd.read_csv("SUN.csv")

euraw, eukal = euler['raw'], euler['kal']
magx, magy = mag['x'], mag['y']
sunx, suny = sun['x'], sun['y']

# Step 1: Division
# plt.figure()
# plt.scatter(magx, magy)
# plt.title("Magnetic Vector")
#
# plt.figure()
# plt.scatter(sunx, suny)
# plt.title("Sun Vector")
#
# plt.figure()
# l1, = plt.plot(magx, label="x")
# l2, = plt.plot(magy, label="y")
# plt.title("Magnetic Vector")
# plt.legend()
#
# plt.figure()
# l1, = plt.plot(sunx, label="x")
# l2, = plt.plot(suny, label="y")
# plt.title("Sun Vector")
# plt.legend()
#
# plt.show()
#
div = [10, 167, 221, 331, 382, 440, 498, 551, 595, 638, 686, 746, 784, 839, 882, 933, 986, 1039, 1108, 1212,
       1259, 1310, 1387, 1500, 1560, 1678, 1735, 1808, 1853, 1886, 1940, 1995, 2050, 2101, 2139, 2197, 2241, 2299]


def getAngles(x, y):
    index = 0
    formerX = 0
    formerY = 0
    angle = []
    while index < len(div) - 2:
        xMean = np.mean(x[div[index]:div[index + 1]])
        yMean = np.mean(y[div[index]:div[index + 1]])
        if index == 0:
            formerX = xMean
            formerY = yMean
        else:
            a = np.array([xMean, yMean])
            b = np.array([formerX, formerY])
            c = np.dot(a, b)
            angle.append(np.arccos(c)/np.pi*180.0)
            # angle.append([formerX, formerY])
            # angle.append([div[index], div[index + 1]])
            formerX = xMean
            formerY = yMean

        index = index + 2

    return angle

magAng = getAngles(magx, magy)
sunAng = getAngles(sunx, suny)

print(magAng)
print(sunAng)

desired = [30, 5, 2.5, 2.5, 2.5, 2.5, 5	, 10, 30, 30, 30, 30, 30, 30, 30, 30, 30]
print(np.mean(np.array(magAng)-np.array(desired)))
print(np.mean(np.array(sunAng)-np.array(desired)))
print(np.mean(np.fabs(np.array(magAng)-np.array(desired))))
print(np.mean(np.fabs(np.array(sunAng)-np.array(desired))))

# plt.figure()
# plt.plot(euraw[1000:1200])
# plt.plot(eukal[1000:1200])

# plt.figure()
# plt.plot(eukal)

plt.show()

