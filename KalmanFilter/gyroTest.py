import matplotlib.pyplot as plt
import serial
import csv

def main():
    # Open serial port to read raw data
    srl = serial.Serial('com18', 38400)

    # imgFile = open("img.csv", 'w')
    # img = csv.writer(imgFile)
    # img.writerow(["x", "y", "z"])
    # imgFile.close()
    #
    # emgFile = open("emg.csv", 'w')
    # emg = csv.writer(emgFile)
    # emg.writerow(["x", "y", "z"])
    # emgFile.close()

    groX = []
    groY = []
    groZ = []
    kgrX = []
    kgrY = []
    kgrZ = []
    while True:
        # 开启matplotlib的交互模式
        plt.ion()

        data = srl.readline()
        data = str(data)

        # Check if the header is completed
        name = ["KGR", "GRO"]
        start = data.find(': ')
        if start == -1:
            continue
        elif data[2:start] not in name:
            continue

        # Check if the rear is completed
        end = data.find('\\r\\n')
        if end == -1:
            continue

        # Extract information
        info = data[start + 2:end]
        head = data[2:start]
        data = [head] + info.split(' ')

        # Internal magnetometer value visualization
        if data[0] == "GRO":

            # IMG's data is incomplete if its length is less than 4
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

            groX.append(data[1])
            groY.append(data[2])
            groZ.append(data[3])

            with open("gro.csv", 'a') as groFile:
                gro = csv.writer(groFile)
                gro.writerow([groX[-1:][0], groY[-1:][0], groZ[-1:][0]])

        # External magnetometer value visualization
        elif data[0] == "KGR":

            # kgr's data is incomplete if its length is less than 4
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

            kgrX.append(data[1])
            kgrY.append(data[2])
            kgrZ.append(data[3])

            with open("kgr.csv", 'a') as kgrFile:
                kgr = csv.writer(kgrFile)
                kgr.writerow([kgrX[-1:][0], kgrY[-1:][0], kgrZ[-1:][0]])

        xFig = plt.figure(1)
        xFig.suptitle("Gyroscope x axis", fontsize=16)
        plt.plot(groX)
        plt.plot(kgrX)

        yFig = plt.figure(2)
        yFig.suptitle("Gyroscope y axis", fontsize=16)
        plt.plot(groY)
        plt.plot(kgrY)

        zFig = plt.figure(3)
        zFig.suptitle("Gyroscope z axis", fontsize=16)
        plt.plot(groZ)
        plt.plot(kgrZ)

        plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

if __name__ == "__main__":
    main()

