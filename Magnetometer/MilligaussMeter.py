import matplotlib.pyplot as plt
import serial
import time
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Open serial port to read raw data
srl = serial.Serial('com17', 115200)

# 开启matplotlib的交互模式
plt.ion()

def getMgmVal(data):

    # Alphaapp manual p10
    s = data[1] & 8
    d = data[1] & 7

    val = ((data[2]<<24) + (data[3]<<16) + (data[4]<<8) + data[5]) / np.power(10.0, d)

    if s == 0:
        return val
    elif s == 8:
        return -val


points = 0
mgmX = []
mgmY = []
mgmZ = []
href = []
while points < 5000:
    srl.write("\x03\x00\x00\x00\x00\x00".encode("UTF-8"))
    # time.sleep(0.5)
    for i in range(5):
        data = []
        for j in range(6):
            d = ord(srl.read(1))
            data.append(d)

        val = getMgmVal(data)
        # print(val)
        if i == 1:
            mgmX.append(val)
        elif i == 2:
            mgmY.append(val)
        elif i == 3:
            mgmZ.append(val)
        elif i == 4:
            href.append(val)
    data = srl.read(1)

    # Data visualization
    mgmFig = plt.figure(1)
    mgmFig.suptitle("Internal magnetometer", fontsize=16)

    x, y, z = mgmX, mgmY, mgmZ
    ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
    #  将数据点分成三部分画，在颜色上有区分度
    ax.scatter(x, y, z, c='b')  # 绘制数据点

    ax.set_zlabel('Z')  # 坐标轴
    ax.set_ylabel('Y')
    ax.set_xlabel('X')

    plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

    points = points + 1

plt.ioff()


