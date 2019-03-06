import matplotlib.pyplot as plt
import serial
from mpl_toolkits.mplot3d import Axes3D
import csv
import _thread

state = 1

def switchState(meiluanyong):
    global state
    while True:
        hand = input("input: ")
        if hand == '1':
            state = 0
        else:
            state = 1
        print(state)


def main():
    global state
    # Open serial port to read raw data
    srl = serial.Serial('com3', 38400)

    _thread.start_new_thread(switchState, ("1234567",))

    imgFile = open("img.csv", 'w')
    img = csv.writer(imgFile)
    img.writerow(["x", "y", "z"])
    imgFile.close()

    emgFile = open("emg.csv", 'w')
    emg = csv.writer(emgFile)
    emg.writerow(["x", "y", "z"])
    emgFile.close()

    imgX = []
    imgY = []
    imgZ = []
    emgX = []
    emgY = []
    emgZ = []
    while True:
        if state == 1:
            # 开启matplotlib的交互模式
            plt.ion()

            data = srl.readline()
            data = str(data)

            # Check if the header is completed
            name = ["EMG", "IMG"]
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
            if data[0] == "IMG":

                # IMG's data is incomplete if its length is less than 4
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

                imgX.append(data[1])
                imgY.append(data[2])
                imgZ.append(data[3])

                with open("img.csv", 'a') as imgFile:
                    img = csv.writer(imgFile)
                    img.writerow([imgX[-1:][0], imgY[-1:][0], imgZ[-1:][0]])

                imgFig = plt.figure(1)
                imgFig.suptitle("Internal magnetometer", fontsize=16)

                x, y, z = imgX, imgY, imgZ
                ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
                #  将数据点分成三部分画，在颜色上有区分度
                ax.scatter(x, y, z, c='b')  # 绘制数据点

                ax.set_zlabel('Z')  # 坐标轴
                ax.set_ylabel('Y')
                ax.set_xlabel('X')

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

            # External magnetometer value visualization
            elif data[0] == "EMG":

                # EMG's data is incomplete if its length is less than 4
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

                emgX.append(data[1])
                emgY.append(data[2])
                emgZ.append(data[3])

                with open("emg.csv", 'a') as emgFile:
                    emg = csv.writer(emgFile)
                    emg.writerow([emgX[-1:][0], emgY[-1:][0], emgZ[-1:][0]])

                emgFig = plt.figure(2)
                emgFig.suptitle("External magnetometer", fontsize=16)

                x, y, z = emgX, emgY, emgZ
                ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
                #  将数据点分成三部分画，在颜色上有区分度
                ax.scatter(x, y, z, c='y')  # 绘制数据点

                ax.set_zlabel('Z')  # 坐标轴
                ax.set_ylabel('Y')
                ax.set_xlabel('X')

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果
        else:
            plt.ioff()

            imgFig = plt.figure(1)
            imgFig.suptitle("Internal magnetometer", fontsize=16)
            x, y, z = imgX, imgY, imgZ
            ax = plt.subplot(111, projection='3d')
            ax.scatter(x, y, z, c='b')
            ax.set_zlabel('Z')
            ax.set_ylabel('Y')
            ax.set_xlabel('X')

            emgFig = plt.figure(2)
            emgFig.suptitle("External magnetometer", fontsize=16)
            x, y, z = emgX, emgY, emgZ
            ax = plt.subplot(111, projection='3d')
            ax.scatter(x, y, z, c='y')
            ax.set_zlabel('Z')
            ax.set_ylabel('Y')
            ax.set_xlabel('X')

            plt.show()



if __name__ == "__main__":
    main()

