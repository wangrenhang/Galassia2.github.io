import serial
import time

RATELIST = [0, 0.5, 2, 5, 10, 8, 3, 0.2, -1, -7, -12, -4, -0.7, 0]

ratetable = serial.Serial('COM16', 9600)
satellite = serial.Serial('COM3', 38400)
file = open(r"MPU6050_validation.txt", 'a')

axis = 'Z'
points = 200
step = 0
rate = 0
while True:
    if step == 0:
        if rate == len(RATELIST):
            break
        cmd= "JOG" + str(RATELIST[rate]) + "\r\n"
        ratetable.write(cmd.encode())
        print(cmd)
        rate = rate + 1

    data = satellite.readline()
    data = str(data)

    file.write(axis + str(RATELIST[rate-1]) + ' ' + data + '\n')
    print(data)

    step = step + 1
    if step == points:
        step = 0


ratetable.write("STO\r\n".encode())
time.sleep(20)
ratetable.write("HOM\r\n".encode())

file.close()
ratetable.close()
satellite.close()


