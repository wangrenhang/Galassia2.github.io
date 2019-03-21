import matplotlib.pyplot as plt
import serial
import csv
import time

param_index = [[0, 0, 0, 0],
               [0, 0, 0, 2],
               [0, 1, 0, 4],
               [0, 0, 1, 1],
               [0, 1, 1, 2],
               [0, 0, 1, 0],
               [0, 1, 0, 0],
               [0, 3, 0, 1],
               [0, 0, 2, 1],
               [0, 0, 2, 0],
               [0, 3, 0, 2],
               [0, 1, 0, 1],
               [0, 0, 0, 3],
               [0, 0, 1, 3],
               [0, 2, 1, 4],
               [0, 1, 1, 1],
               [0, 4, 3, 0],
               [0, 2, 0, 3],
               [0, 2, 0, 1],
               [0, 0, 2, 2]]

param_table = {"kf_trust_gyro": [2, 5, 10, 50, 100], "kf_trust_quat": [2, 5, 10, 50, 100],
               "kf_w_thres": [0.01, 0.02, 0.05, 0.1, 0.5], "kf_deltaT": [0.21, 0.22, 0.23, 0.24, 0.25]}

def writeMsg(srl, msg):
    print(msg)
    srl.write(msg)
    time.sleep(1)

def setParam(srl, a, b, c, d):
    msg = str(param_table["kf_trust_gyro"][a]).encode()
    writeMsg(srl, b"param set kf_trust_gyro " + msg + b"\r\n")

    msg = str(param_table["kf_trust_quat"][b]).encode()
    writeMsg(srl, b"param set kf_trust_quat " + msg + b"\r\n")

    msg = str(param_table["kf_w_thres"][c]).encode()
    writeMsg(srl, b"param set kf_w_thres " + msg + b"\r\n")

    msg = str(param_table["kf_deltaT"][d]).encode()
    writeMsg(srl, b"param set kf_deltaT " + msg + b"\r\n")


def main():

    EulerFile = open("euler.csv", 'w')
    euler = csv.writer(EulerFile)
    euler.writerow(["yaw", "pitch", "roll", "p1", "p2", "p3", "p4"])
    EulerFile.close()

    EukalFile = open("eukal.csv", 'w')
    eukal = csv.writer(EukalFile)
    eukal.writerow(["yaw", "pitch", "roll", "p1", "p2", "p3", "p4"])
    EukalFile.close()

    # Open serial port to read raw data
    with serial.Serial('com18', 38400) as srl:

        writeMsg(srl, b"param mem 8\r\n")
        writeMsg(srl, b"param set set_inertial 1\r\n")
        time.sleep(5)

        a = 0
        while True:
            setParam(srl, param_index[a][0], param_index[a][1], param_index[a][2], param_index[a][3])
            writeMsg(srl, b"param set print_ads 5\r\n")

            ticks = time.time()
            while time.time() - ticks < 10:
                data = srl.readline()
                data = str(data)
                print(data)

                # Check if the header is completed
                name = ["Euler", "Euler Kal"]
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

                # Raw Euler angle
                if data[0] == "Euler":

                    # quat's data is incomplete if its length is less than 5
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

                    with open("euler.csv", 'a') as eulerFile:
                        euler = csv.writer(eulerFile)
                        euler.writerow([data[1], data[2], data[3], param_index[a][0], param_index[a][1], param_index[a][2], param_index[a][3]])

                # Raw Euler angle
                if data[0] == "Euler Kal":

                    # quat's data is incomplete if its length is less than 5
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

                    with open("eukal.csv", 'a') as eukalFile:
                        eukal = csv.writer(eukalFile)
                        eukal.writerow([data[1], data[2], data[3], param_index[a][0], param_index[a][1], param_index[a][2], param_index[a][3]])

            writeMsg(srl, b"param set print_ads 0\r\n")
            a = a + 1
            if a > len(param_index) - 1:
                break;

if __name__ == "__main__":
    main()