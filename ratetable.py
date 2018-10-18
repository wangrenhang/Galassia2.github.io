# To calibrate the gyroscope, there should be a ratetable to offer standard and stable angular velocity.
# Then, some algorithms can calibrate the output of the gyro's to fit in the standard value of the ratetable.
# This file is used to control the ratetable, and read the satellite's uploading data
import serial
import time

# Angular velocity adopted to calibrate the gyroscope
RATELIST = [0, 0.1, 0.2, 0.3, 0.4, 0.6, 0.8, 1, 2, 3, 4, 6, 8, 10, 15, 20, 25, 30,
           0, -0.1, -0.2, -0.3, -0.4, -0.6, -0.8, -1, -2, -3, -4, -6, -8, -10, -15, -20, -25, -30]
#RATELIST = [2, 3, 4, -2]

# Obtain 500 points, enough for calibration
points = 500
# Gyro has 3 axis to calibrate, change the axis here.
axis = 'Z'

ratetable = serial.Serial('COM16', 9600)
satellite = serial.Serial('COM3', 38400)
file = open(r"MPU3300.txt", 'a')

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
        # time.sleep(10)

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

