import numpy as np
import matplotlib.pyplot as plt
import serial
import csv
import _thread

# Choose one sensor to show its output
sensorToShow = 6

def dataExtract(data):

    name = ["FSS", "CST", "CSV", "IMG", "EMG", "GRO"]

    # Check if the header is completed
    start = data.find(': ')
    if start == -1:
        return -1
    elif data[2:start] not in name:
        return -1

    # Check if the rear is completed
    end = data.find('\\r\\n')
    if end == -1:
        return -1

    # Extract information
    info = data[start+2:end]
    head = data[2:start]
    data = [head] + info.split(' ')

    return data

def abnormalProcess(data, propRange):

    for i in range(len(data)):
        if i == 0:
            continue
        else:
            if data[i] < float(propRange[i-1][0]) or data[i] > float(propRange[i-1][1]):
                print(str(data)+" "+str(propRange[i-1][0])+" "+str(propRange[i-1][1]))
                filename = str(data[0]) + "error.txt"
                errFile = open(filename, 'a')
                errFile.write(str(data)+'\n')
                errFile.close()
                return -1
    return 1

def switchImg(threadName):
    global sensorToShow

    while True:
        try:
            num = input("Sensor number to show: ")
            num = ord(num)
            if num > ord('0') and num < ord('7'):
                sensorToShow = num - ord('0')
        except TypeError:
            continue


def main():

    # Open serial port to read raw data
    srl = serial.Serial('com3', 38400)

    # Open CSV files
    fssFile = open("FSS.csv", 'w')
    cstFile = open("CST.csv", 'w')
    csvFile = open("CSV.csv", 'w')
    imgFile = open("IMG.csv", 'w')
    emgFile = open("EMG.csv", 'w')
    groFile = open("GRO.csv", 'w')

    # Initial CSV writers
    fss = csv.writer(fssFile)
    cst = csv.writer(cstFile)
    csu = csv.writer(csvFile)
    img = csv.writer(imgFile)
    emg = csv.writer(emgFile)
    gro = csv.writer(groFile)

    # Write CSV header first
    fss.writerow(["theta", "phi", "temp"])
    cst.writerow(["t1", "t2", "t3", "t4"])
    csu.writerow(["v1", "v2", "v3", "v4"])
    img.writerow(["mx", "my", "mz"])
    emg.writerow(["mx", "my", "mz", "temp"])
    gro.writerow(["x", "y", "z", "temp"])

    fssFile.close()
    cstFile.close()
    csvFile.close()
    imgFile.close()
    emgFile.close()
    groFile.close()

    # 开启matplotlib的交互模式
    plt.ion()

    # FSS data storage
    fssTheta = []
    fssPhi = []
    fssT = []
    fssCnt = 0

    # CST data storage
    cst1 = []
    cst2 = []
    cst3 = []
    cst4 = []
    cstCnt = 0

    # CSV data storage
    csv1 = []
    csv2  = []
    csv3 = []
    csv4 = []
    csvCnt = 0

    # IMG data storage
    imgX = []
    imgY = []
    imgZ = []
    imgCnt = 0

    # EMG data storage
    emgX = []
    emgY = []
    emgZ = []
    emgT = []
    emgCnt = 0

    # Gyro data storage
    groX = []
    groY = []
    groZ = []
    groT = []
    groCnt = 0

    # Switch which sensor's output to show
    _thread.start_new_thread(switchImg, ("Thread-SwitchSensor",))

    while True:

        data = srl.readline()
        data = str(data)

        # Do data cleaning, eliminate incomplete lines but reserve corrupted data for further analyzing
        # Extract useful information from the cleaned raw input data
        data = dataExtract(data)
        if data == -1:
            continue

        # Fine sun sensor visualization
        if data[0] == "FSS":

            # Fine sun sensor's data is incomplete if its length is less than 4
            if len(data) != 4:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            # If some value exceed its proper range, it will be written to an error log
            normal = abnormalProcess(data, [[-2, 8], [-2, 8], [-100, 100]])

            # Write to CSV file
            if normal == 1:
                with open("FSS.csv", 'a') as fssFile:
                    fss = csv.writer(fssFile)
                    fss.writerow(data[1:])

            if sensorToShow == 1:

                fssFig = plt.figure(1)
                fssFig.suptitle("Fine sun sensor", fontsize = 16)

                fssThetaFig = plt.subplot(131)
                fssThetaFig.set_title("Theta")
                plt.xlim([fssCnt * 100, fssCnt * 100 + 100])
                plt.ylim([-2, 8])
                fssTheta.append(data[1])
                plt.plot(range(fssCnt * 100, fssCnt * 100 + 100)[:len(fssTheta)], fssTheta)  # 将list传入plot画图

                fssPhiFig = plt.subplot(132)
                fssPhiFig.set_title("Phi")
                plt.xlim([fssCnt * 100, fssCnt * 100 + 100])
                plt.ylim([-2, 8])
                fssPhi.append(data[2])
                plt.plot(range(fssCnt * 100, fssCnt * 100 + 100)[:len(fssPhi)], fssPhi)  # 将list传入plot画图

                fssTfig = plt.subplot(133)
                fssTfig.set_title("Temperature")
                plt.xlim([fssCnt * 100, fssCnt * 100 + 100])
                plt.ylim([-100, 100])
                fssT.append(data[3])
                plt.plot(range(fssCnt * 100, fssCnt * 100 + 100)[:len(fssT)], fssT)  # 将list传入plot画图

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

                if len(fssT) >= 100:
                    fssTheta = []
                    fssPhi = []
                    fssT = []
                    plt.clf()
                    fssCnt = fssCnt + 1

            else:
                plt.close(1)

        # Coarse sun sensor temperature visualization
        elif data[0] == "CST":

            # CST's data is incomplete if its length is less than 5
            if len(data) != 5:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            # If some value exceed its proper range, it will be written to an error log
            normal = abnormalProcess(data, [[-100, 100], [-100, 100], [-100, 100], [-100, 100]])

            # Write to CSV file
            if normal == 1:
                with open("CST.csv", 'a') as cstFile:
                    cst = csv.writer(cstFile)
                    cst.writerow(data[1:])

            if sensorToShow == 2:

                cstFig = plt.figure(2)
                cstFig.suptitle("Coarse sun sensor temperature", fontsize = 16)

                cst1fig = plt.subplot(221)
                cst1fig.set_title("CST1")
                plt.xlim([cstCnt * 100, cstCnt * 100 + 100])
                plt.ylim([-100, 100])
                cst1.append(data[1])
                plt.plot(range(cstCnt * 100, cstCnt * 100 + 100)[:len(cst1)], cst1)  # 将list传入plot画图

                cst2fig = plt.subplot(222)
                cst2fig.set_title("CST2")
                plt.xlim([cstCnt * 100, cstCnt * 100 + 100])
                plt.ylim([-100, 100])
                cst2.append(data[2])
                plt.plot(range(cstCnt * 100, cstCnt * 100 + 100)[:len(cst2)], cst2)  # 将list传入plot画图

                cst1fig = plt.subplot(223)
                cst1fig.set_title("CST3")
                plt.xlim([cstCnt * 100, cstCnt * 100 + 100])
                plt.ylim([-100, 100])
                cst3.append(data[3])
                plt.plot(range(cstCnt * 100, cstCnt * 100 + 100)[:len(cst3)], cst3)  # 将list传入plot画图

                cst1fig = plt.subplot(224)
                cst1fig.set_title("CST4")
                plt.xlim([cstCnt * 100, cstCnt * 100 + 100])
                plt.ylim([-100, 100])
                cst4.append(data[4])
                plt.plot(range(cstCnt * 100, cstCnt * 100 + 100)[:len(cst4)], cst4)  # 将list传入plot画图

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

                if len(cst4) >= 100:
                    cst1 = []
                    cst2 = []
                    cst3 = []
                    cst4 = []
                    plt.clf()
                    cstCnt = cstCnt + 1

            else:
                plt.close(2)

        # Coarse sun sensor value visualization
        elif data[0] == "CSV":

            # CSV's data is incomplete if its length is less than 5
            if len(data) != 5:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            # If some value exceed its proper range, it will be written to an error log
            normal = abnormalProcess(data, [[-0.25, 0.25], [-0.25, 0.25], [-0.25, 0.25], [-0.25, 0.25]])

            # Write to CSV file
            if normal == 1:
                with open("CSV.csv", 'a') as csvFile:
                    csu = csv.writer(csvFile)
                    csu.writerow(data[1:])

            if sensorToShow == 3:

                csvFig = plt.figure(3)
                csvFig.suptitle("Coarse sun sensor value", fontsize=16)

                csv1fig = plt.subplot(221)
                csv1fig.set_title("CSV1")
                plt.xlim([csvCnt * 100, csvCnt * 100 + 100])
                plt.ylim([-0.25, 0.25])
                csv1.append(data[1])
                plt.plot(range(csvCnt * 100, csvCnt * 100 + 100)[:len(csv1)], csv1)  # 将list传入plot画图

                csv2fig = plt.subplot(222)
                csv2fig.set_title("CSV2")
                plt.xlim([csvCnt * 100, csvCnt * 100 + 100])
                plt.ylim([-0.25, 0.25])
                csv2.append(data[2])
                plt.plot(range(csvCnt * 100, csvCnt * 100 + 100)[:len(csv2)], csv2)  # 将list传入plot画图

                csv3fig = plt.subplot(223)
                csv3fig.set_title("CSV3")
                plt.xlim([csvCnt * 100, csvCnt * 100 + 100])
                plt.ylim([-0.25, 0.25])
                csv3.append(data[3])
                plt.plot(range(csvCnt * 100, csvCnt * 100 + 100)[:len(csv3)], csv3)  # 将list传入plot画图

                csv4fig = plt.subplot(224)
                csv4fig.set_title("CSV4")
                plt.xlim([csvCnt * 100, csvCnt * 100 + 100])
                plt.ylim([-0.25, 0.25])
                csv4.append(data[4])
                plt.plot(range(csvCnt * 100, csvCnt * 100 + 100)[:len(csv4)], csv4)  # 将list传入plot画图

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

                if len(csv4) >= 100:
                    csv1 = []
                    csv2 = []
                    csv3 = []
                    csv4 = []
                    plt.clf()
                    csvCnt = csvCnt + 1

            else:
                plt.close(3)

        # Internal magnetometer value visualization
        elif data[0] == "IMG":

            # CSV's data is incomplete if its length is less than 4
            if len(data) != 4:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            # If some value exceed its proper range, it will be written to an error log
            normal = abnormalProcess(data, [[-1500, 1500], [-1500, 1500], [-1500, 1500], [-1500, 1500]])

            # Write to CSV file
            if normal == 1:
                with open("IMG.csv", 'a') as imgFile:
                    img = csv.writer(imgFile)
                    img.writerow(data[1:])

            if sensorToShow == 4:

                imgFig = plt.figure(4)
                imgFig.suptitle("Internal magnetometer", fontsize=16)

                imgXfig = plt.subplot(131)
                imgXfig.set_title("X Axis")
                plt.xlim([imgCnt * 100, imgCnt * 100 + 100])
                plt.ylim([-1500, 1500])
                imgX.append(data[1])
                plt.plot(range(imgCnt * 100, imgCnt * 100 + 100)[:len(imgX)], imgX)  # 将list传入plot画图

                imgYfig = plt.subplot(132)
                imgYfig.set_title("Y Axis")
                plt.xlim([imgCnt * 100, imgCnt * 100 + 100])
                plt.ylim([-1500, 1500])
                imgY.append(data[2])
                plt.plot(range(imgCnt * 100, imgCnt * 100 + 100)[:len(imgY)], imgY)  # 将list传入plot画图

                imgZfig = plt.subplot(133)
                imgZfig.set_title("Z Axis")
                plt.xlim([imgCnt * 100, imgCnt * 100 + 100])
                plt.ylim([-1500, 1500])
                imgZ.append(data[3])
                plt.plot(range(imgCnt * 100, imgCnt * 100 + 100)[:len(imgZ)], imgZ)  # 将list传入plot画图

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

                if len(imgZ) >= 100:
                    imgX = []
                    imgY = []
                    imgZ = []
                    plt.clf()
                    imgCnt = imgCnt + 1

            else:
                plt.close(4)

        # External magnetometer value visualization
        elif data[0] == "EMG":

            # CSV's data is incomplete if its length is less than 4
            if len(data) != 5:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            # If some value exceed its proper range, it will be written to an error log
            normal = abnormalProcess(data, [[-1500, 1500], [-1500, 1500], [-1500, 1500], [-1500, 1500], [-100, 100]])

            # Write to CSV file
            if normal == 1:
                with open("EMG.csv", 'a') as emgFile:
                    emg = csv.writer(emgFile)
                    emg.writerow(data[1:])

            if sensorToShow == 5:

                emgFig = plt.figure(5)
                emgFig.suptitle("External magnetometer", fontsize = 16)

                emgXfig = plt.subplot(221)
                emgXfig.set_title("X Axis")
                plt.xlim([emgCnt * 100, emgCnt * 100 + 100])
                plt.ylim([-1500, 1500])
                emgX.append(data[1])
                plt.plot(range(emgCnt * 100, emgCnt * 100 + 100)[:len(emgX)], emgX)  # 将list传入plot画图

                emgYfig = plt.subplot(222)
                emgYfig.set_title("Y Axis")
                plt.xlim([emgCnt * 100, emgCnt * 100 + 100])
                plt.ylim([-1500, 1500])
                emgY.append(data[2])
                plt.plot(range(emgCnt * 100, emgCnt * 100 + 100)[:len(emgY)], emgY)  # 将list传入plot画图

                emgZfig = plt.subplot(223)
                emgZfig.set_title("Z Axis")
                plt.xlim([emgCnt * 100, emgCnt * 100 + 100])
                plt.ylim([-1500, 1500])
                emgZ.append(data[3])
                plt.plot(range(emgCnt * 100, emgCnt * 100 + 100)[:len(emgZ)], emgZ)  # 将list传入plot画图

                emgTfig = plt.subplot(224)
                emgTfig.set_title("Temperature")
                plt.xlim([emgCnt * 100, emgCnt * 100 + 100])
                plt.ylim([-100, 100])
                emgT.append(data[4])
                plt.plot(range(emgCnt * 100, emgCnt * 100 + 100)[:len(emgT)], emgT)  # 将list传入plot画图

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

                if len(emgT) >= 100:
                    emgX = []
                    emgY = []
                    emgZ = []
                    emgT = []
                    plt.clf()
                    emgCnt = emgCnt + 1

            else:
                plt.close(5)

        # Gyroscope visualization
        elif data[0] == "GRO":

            # Gyro's data is incomplete if its length is less than 5
            if len(data) != 5:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            # If some value exceed its proper range, it will be written to an error log
            normal = abnormalProcess(data, [[-10, 10], [-10, 10], [-10, 10], [-100, 100]])

            # Write to CSV file
            if normal == 1:
                with open("GRO.csv", 'a') as groFile:
                    gro = csv.writer(groFile)
                    gro.writerow(data[1:])

            if sensorToShow == 6:

                groFig = plt.figure(6)
                groFig.suptitle("Gyroscope", fontsize = 16)

                gyroXfig = plt.subplot(221)
                gyroXfig.set_title("X axis")
                plt.xlim([groCnt * 100, groCnt * 100 + 100])
                plt.ylim([-10, 10])
                groX.append(data[1])
                plt.plot(range(groCnt * 100, groCnt * 100 + 100)[:len(groX)], groX)  # 将list传入plot画图

                gyroYfig = plt.subplot(222)
                gyroYfig.set_title("Y axis")
                plt.xlim([groCnt * 100, groCnt * 100 + 100])
                plt.ylim([-10, 10])
                groY.append(data[2])
                plt.plot(range(groCnt * 100, groCnt * 100 + 100)[:len(groY)], groY)  # 将list传入plot画图

                gyroZfig = plt.subplot(223)
                gyroZfig.set_title("Z axis")
                plt.xlim([groCnt * 100, groCnt * 100 + 100])
                plt.ylim([-10, 10])
                groZ.append(data[3])
                plt.plot(range(groCnt * 100, groCnt * 100 + 100)[:len(groZ)], groZ)  # 将list传入plot画图

                gyroTfig = plt.subplot(224)
                gyroTfig.set_title("Temperature")
                plt.xlim([groCnt * 100, groCnt * 100 + 100])
                plt.ylim([-100, 100])
                groT.append(data[4])
                plt.plot(range(groCnt * 100, groCnt * 100 + 100)[:len(groT)], groT)  # 将list传入plot画图

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

                if len(groZ) >= 100:
                    groX = []
                    groY = []
                    groZ = []
                    groT = []
                    plt.clf()
                    groCnt = groCnt + 1

            else:
                plt.close(6)

        else:
            continue


if __name__ == "__main__":
    main()