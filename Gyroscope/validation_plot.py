import numpy as np
import matplotlib.pyplot as plt
import csv

csvData = open(r"MPU6050_validation.csv", 'r')
csvDict = csv.DictReader(csvData)

# Sensor,Axis,Angular velocity,X,Y,Z,Temp
onePeriod = []
filteredData = []
previousAV = 0
for line in csvDict:
    if line["Angular velocity"] != previousAV:
        # Get rid of first 20 data and last 4 data
        filteredData.extend(onePeriod[20:-4])
        previousAV = line["Angular velocity"]
        onePeriod = []
    else:
        onePeriod.append(line)
csvData.close()

ext = []
extStd = []
extIndex = []
extindex = 0
kal = []
kalStd = []
kalIndex = []
kalindex = 0
for line in filteredData:
    if line["Sensor"] == "EXT":
        ext.extend([float(line["X"]), float(line["Y"]), float(line["Z"])])
        extIndex.append(extindex)
        extindex = extindex + 1
        if line["Axis"] == 'X':
            extStd.extend([float(line["Angular velocity"]), 0.0, 0.0])
        elif line["Axis"] == 'Y':
            extStd.extend([0.0, float(line["Angular velocity"]), 0.0])
        elif line["Axis"] == 'Z':
            extStd.extend([0.0, 0.0, float(line["Angular velocity"])])
    elif line["Sensor"] == "Kal":
        kal.extend([float(line["X"]), float(line["Y"]), float(line["Z"])])
        kalIndex.append(kalindex)
        kalindex = kalindex + 1
        if line["Axis"] == 'X':
            kalStd.extend([float(line["Angular velocity"]), 0.0, 0.0])
        elif line["Axis"] == 'Y':
            kalStd.extend([0.0, float(line["Angular velocity"]), 0.0])
        elif line["Axis"] == 'Z':
            kalStd.extend([0.0, 0.0, float(line["Angular velocity"])])

def fetch(dataList, axis):
    length = len(dataList) // 3
    temp = []
    for i in range(length):
        temp.append(dataList[3*i+int(ord(axis)-ord('x'))])
    return temp

plt.figure(1)
l1, = plt.plot(extIndex, fetch(ext, 'x'), color='red', linewidth=1.0, linestyle='--')
l2, = plt.plot(extIndex, fetch(ext, 'y'), color='green', linewidth=1.0, linestyle='-')
l3, = plt.plot(extIndex, fetch(ext, 'z'), color='blue', linewidth=1.0, linestyle='-.')
plt.legend(handles = [l1, l2, l3,], labels = ['X axis', 'Y axis', 'Z axis'], loc = 'best')
plt.title('Before Kalman Filter')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')

plt.figure(2)
l1, = plt.plot(kalIndex, fetch(kal, 'x'), color='red', linewidth=1.0, linestyle='--')
l2, = plt.plot(kalIndex, fetch(kal, 'y'), color='green', linewidth=1.0, linestyle='-')
l3, = plt.plot(kalIndex, fetch(kal, 'z'), color='blue', linewidth=1.0, linestyle='-.')
plt.legend(handles = [l1, l2, l3,], labels = ['X axis', 'Y axis', 'Z axis'], loc = 'best')
plt.title('After Kalman Filter')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')

plt.figure(3)
plt.subplot(121)
l1, = plt.plot(extIndex[:1000], fetch(extStd, 'x')[:1000], color='red', linewidth=3.0, linestyle='--')
l2, = plt.plot(extIndex[:1000], fetch(ext, 'x')[:1000], color='blue', linewidth=1.0, linestyle='-')
plt.legend(handles = [l1, l2], labels = ['Standard value', 'Measured value'], loc = 'best')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')
plt.title('X Axis Before Kalman Filter')
plt.subplot(122)
l1, = plt.plot(kalIndex[:1000], fetch(kalStd, 'x')[:1000], color='red', linewidth=3.0, linestyle='--')
l2, = plt.plot(kalIndex[:1000], fetch(kal, 'x')[:1000], color='blue', linewidth=1.0, linestyle='-')
plt.legend(handles = [l1, l2], labels = ['Standard value', 'Filtered value'], loc = 'best')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')
plt.title('X Axis After Kalman Filter')

plt.figure(4)
plt.subplot(121)
l1, = plt.plot(extIndex[1500:2500], fetch(extStd, 'y')[1500:2500], color='red', linewidth=3.0, linestyle='--')
l2, = plt.plot(extIndex[1500:2500], fetch(ext, 'y')[1500:2500], color='blue', linewidth=1.0, linestyle='-')
plt.legend(handles = [l1, l2], labels = ['Standard value', 'Measured value'], loc = 'best')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')
plt.title('Y Axis Before Kalman Filter')
plt.subplot(122)
l1, = plt.plot(kalIndex[1500:2500], fetch(kalStd, 'y')[1500:2500], color='red', linewidth=3.0, linestyle='--')
l2, = plt.plot(kalIndex[1500:2500], fetch(kal, 'y')[1500:2500], color='blue', linewidth=1.0, linestyle='-')
plt.legend(handles = [l1, l2], labels = ['Standard value', 'Filtered value'], loc = 'best')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')
plt.title('Y Axis After Kalman Filter')

plt.figure(5)
plt.subplot(121)
l1, = plt.plot(extIndex[2500:3500], fetch(extStd, 'z')[2500:3500], color='red', linewidth=3.0, linestyle='--')
l2, = plt.plot(extIndex[2500:3500], fetch(ext, 'z')[2500:3500], color='blue', linewidth=1.0, linestyle='-')
plt.legend(handles = [l1, l2], labels = ['Standard value', 'Measured value'], loc = 'best')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')
plt.title('Z Axis Before Kalman Filter')
plt.subplot(122)
l1, = plt.plot(kalIndex[2500:3500], fetch(kalStd, 'z')[2500:3500], color='red', linewidth=3.0, linestyle='--')
l2, = plt.plot(kalIndex[2500:3500], fetch(kal, 'z')[2500:3500], color='blue', linewidth=1.0, linestyle='-')
plt.legend(handles = [l1, l2], labels = ['Standard value', 'Filtered value'], loc = 'best')
plt.xlabel('Sample point')
plt.ylabel('Value/ (degree/s)')
plt.title('Z Axis After Kalman Filter')

plt.show()

def getDeviation(dataList, stdList, axis):
    extErr = 0
    extVar = 0
    extDev = 0
    length = len(dataList) // 3
    for i in range(length):
        extErr = extErr + abs(dataList[3*i+int(ord(axis)-ord('x'))] - stdList[3*i+int(ord(axis)-ord('x'))])
        extVar = extVar + (dataList[3*i+int(ord(axis)-ord('x'))] - stdList[3*i+int(ord(axis)-ord('x'))]) ** 2
    extErr = extErr / length
    extVar = extVar / length
    extDev = np.sqrt(extVar)
    print(axis + " Average deviation:" + str(extErr))
    print(axis + " Variance:" + str(extVar))
    print(axis + " Standard deviation:" + str(extDev))

print("Before:")
getDeviation(ext, extStd, 'x')
getDeviation(ext, extStd, 'y')
getDeviation(ext, extStd, 'z')
print("After:")
getDeviation(kal, kalStd, 'x')
getDeviation(kal, kalStd, 'y')
getDeviation(kal, kalStd, 'z')


