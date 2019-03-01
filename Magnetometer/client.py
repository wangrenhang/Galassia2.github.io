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

def main():
    global datardy, mgmdata
    SERVER_IP = "172.23.231.233"
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
            print("Can't connect to server,try it latter!")
            time.sleep(0.1)
            continue
    print("Connection succeeded.")

    _thread.start_new_thread(sockSend, (socket_tcp,))
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


if __name__ == "__main__":
    main()