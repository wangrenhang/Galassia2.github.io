import socket
import time
import sys
import _thread
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

datardy = 0
mgmdata = []

def sockSend(socket_tcp):
    while True:
        try:
            command = input()
            socket_tcp.send(command.encode())
            time.sleep(0.1)
            continue
        except Exception:
            socket_tcp.close()
            socket_tcp = None
            sys.exit(1)

def sockRecv(socket_tcp):
    global datardy, mgmdata
    while True:
        try:
            data = socket_tcp.recv(512)
            if len(data) > 0:
                # print("Received: %s" % data.decode("UTF-8"))
                data = data.decode("UTF-8")
                if data.find('[') != -1 and data.find(']') != -1:
                    mgmdata = []
                    for i in range(3):
                        comma = data.find(',')
                        mgmdata.append(float(data[1:comma]))
                        data = data[comma+1:]
                    end = data.find(']')
                    mgmdata.append(float(data[1:end]))
                    datardy = 1
                else:
                    print(data)
                continue

        except Exception:
            socket_tcp.close()
            socket_tcp = None
            sys.exit(1)

x = []
y = []
z = []
def main():
    global datardy, mgmdata
    SERVER_IP = "172.17.189.33"
    SERVER_PORT = 8888
    print("Starting socket: TCP...")
    server_addr = (SERVER_IP, SERVER_PORT)
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
            socket_tcp.connect(server_addr)
            break
        except Exception:
            print("Can't connect to server,try it later!")
            time.sleep(0.1)
            continue
    print("Connection succeeded.")

    # _thread.start_new_thread(sockSend, (socket_tcp,))
    _thread.start_new_thread(sockRecv, (socket_tcp,))

    mgmFile = open("mgm.csv", 'w')
    mgm = csv.writer(mgmFile)
    mgm.writerow(["x", "y", "z", "h"])
    mgmFile.close()

    while True:
        if datardy == 1:
            datardy = 0
            with open("mgm.csv", 'a') as mgmFile:
                mgm = csv.writer(mgmFile)
                mgm.writerow(mgmdata)

                # Data visualization
                mgmFig = plt.figure(1)
                mgmFig.suptitle("Internal magnetometer", fontsize=16)

                x.append(mgmdata[0])
                y.append(mgmdata[1])
                z.append(mgmdata[2])
                ax = plt.subplot(111, projection='3d')  # 创建一个三维的绘图工程
                #  将数据点分成三部分画，在颜色上有区分度
                ax.scatter(x, y, z, c='b')  # 绘制数据点

                ax.set_zlabel('Z')  # 坐标轴
                ax.set_ylabel('Y')
                ax.set_xlabel('X')

                plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果


if __name__ == "__main__":
    main()