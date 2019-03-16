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
    srl = serial.Serial('com18', 38400)

    _thread.start_new_thread(switchState, ("1234567",))

    quatFile = open("quat.csv", 'w')
    quat = csv.writer(quatFile)
    quat.writerow(["w", "x", "y", "z"])
    quatFile.close()

    kalqFile = open("kalq.csv", 'w')
    kalq = csv.writer(kalqFile)
    kalq.writerow(["w", "x", "y", "z"])
    kalqFile.close()

    EulerFile = open("euler.csv", 'w')
    euler = csv.writer(EulerFile)
    euler.writerow(["yaw", "pitch", "roll"])
    EulerFile.close()

    EukalFile = open("eukal.csv", 'w')
    eukal = csv.writer(EukalFile)
    eukal.writerow(["yaw", "pitch", "roll"])
    EukalFile.close()

    # Data storage
    quatW = []
    quatZ = []
    kalqW = []
    kalqZ = []
    euler = []
    eukal = []
    while True:
        if state == 1:
            # 开启matplotlib的交互模式
            plt.ion()

            data = srl.readline()
            data = str(data)

            # Check if the header is completed
            name = ["Quat Kal", "Quat", "Euler", "Euler Kal"]
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

            # Raw quaternion visualization
            if data[0] == "Quat":

                # quat's data is incomplete if its length is less than 5
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

                quatW.append(data[1])
                quatZ.append(data[4])

                with open("quat.csv", 'a') as quatFile:
                    quat = csv.writer(quatFile)
                    quat.writerow([quatW[-1:][0], 0, 0, quatZ[-1:][0]])

                # quatFig = plt.figure(1)
                # quatFig.suptitle("Raw Quaternion", fontsize=16)
                #
                # index = [i for i in range(len(quatW))]
                # lqw, = plt.plot(index, quatW, color='red')
                # lqz, = plt.plot(index, quatZ, color='blue')
                # plt.legend(handles=[lqw, lqz, ], labels=['w', 'z'], loc='best')
                # plt.xlabel('Data Points')
                # plt.ylabel('Quaternion')
                #
                # plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

            # External magnetometer value visualization
            elif data[0] == "Quat Kal":

                # kalq's data is incomplete if its length is less than 5
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

                kalqW.append(data[1])
                kalqZ.append(data[4])

                with open("kalq.csv", 'a') as kalqFile:
                    kalq = csv.writer(kalqFile)
                    kalq.writerow([kalqW[-1:][0], 0, 0, kalqZ[-1:][0]])

                # kalqFig = plt.figure(2)
                # kalqFig.suptitle("Filtered Quaternion", fontsize=16)
                #
                # index = [i for i in range(len(kalqW))]
                # lkw, = plt.plot(index, kalqW,  color='red')
                # lkz, = plt.plot(index, kalqZ,  color='blue')
                # plt.legend(handles=[lkw, lkz, ], labels=['w', 'z'], loc='best')
                # plt.xlabel('Data Points')
                # plt.ylabel('Quaternion')
                #
                # plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

            else:
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

                if data[0] == "Euler":
                    euler.append(data[1])
                    with open("euler.csv", 'a') as eulerFile:
                        eu = csv.writer(eulerFile)
                        eu.writerow([data[1], data[2], data[3]])
                elif data[0] == "Euler Kal":
                    eukal.append(data[1])
                    with open("eukal.csv", 'a') as eukalFile:
                        ek = csv.writer(eukalFile)
                        ek.writerow([data[1], data[2], data[3]])

            # wFig = plt.figure(3)
            # wFig.suptitle("w data", fontsize=16)
            # index1 = [i for i in range(len(quatW))]
            # index2 = [i for i in range(len(kalqW))]
            # lqw, = plt.plot(index1, quatW, color='red')
            # lkw, = plt.plot(index2, kalqW, color='blue')
            # plt.legend(handles=[lqw, lkw, ], labels=['Raw Quat', 'Filtered'], loc='best')
            # plt.xlabel('Data Points')
            # plt.ylabel('Quaternion')
            # plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果
            #
            # zFig = plt.figure(4)
            # zFig.suptitle("z data", fontsize=16)
            # index1 = [i for i in range(len(quatZ))]
            # index2 = [i for i in range(len(kalqZ))]
            # lqz, = plt.plot(index1, quatZ, color='red')
            # lkz, = plt.plot(index2, kalqZ, color='blue')
            # plt.legend(handles=[lqz, lkz, ], labels=['Raw Quat', 'Filtered'], loc='best')
            # plt.xlabel('Data Points')
            # plt.ylabel('Quaternion')
            # plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

            eFig = plt.figure(5)
            eFig.suptitle("Euler Angle (Yaw)", fontsize=16)
            index1 = [i for i in range(len(euler))]
            index2 = [i for i in range(len(eukal))]
            leu, = plt.plot(index1, euler, color='red')
            lek, = plt.plot(index2, eukal, color='blue')
            plt.legend(handles=[leu, lek, ], labels=['Raw Yaw', 'Filtered'], loc='best')
            plt.xlabel('Data Points')
            plt.ylabel('Yaw / °')
            plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

        else:
            plt.ioff()

            quatFig = plt.figure(1)
            quatFig.suptitle("Raw Quaternion", fontsize=16)
            index = [i for i in range(len(quatW))]
            lqw, = plt.plot(index, quatW, color='red')
            lqz, = plt.plot(index, quatZ, color='blue')
            plt.legend(handles=[lqw, lqz, ], labels=['w', 'z'], loc='best')
            plt.xlabel('Data Points')
            plt.ylabel('Quaternion')

            kalqFig = plt.figure(2)
            kalqFig.suptitle("Filtered Quaternion", fontsize=16)
            index = [i for i in range(len(kalqW))]
            lkw, = plt.plot(index, kalqW, color='red')
            lkz, = plt.plot(index, kalqZ, color='blue')
            plt.legend(handles=[lkw, lkz, ], labels=['w', 'z'], loc='best')
            plt.xlabel('Data Points')
            plt.ylabel('Quaternion')

            eFig = plt.figure(5)
            eFig.suptitle("Euler Angle (Yaw)", fontsize=16)
            index1 = [i for i in range(len(euler))]
            index2 = [i for i in range(len(eukal))]
            leu, = plt.plot(index1, euler, color='red')
            lek, = plt.plot(index2, eukal, color='blue')
            plt.legend(handles=[leu, lek, ], labels=['Raw Yaw', 'Filtered'], loc='best')
            plt.xlabel('Data Points')
            plt.ylabel('Yaw / °')

            plt.show()



if __name__ == "__main__":
    main()



