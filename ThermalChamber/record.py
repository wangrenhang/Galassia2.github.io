import serial

serial = serial.Serial('com3', 38400)
with open(r"ThermalChamber.txt", 'a') as f:
    while True:
        data = serial.readline()
        data = str(data)
        print(data)
        f.write(data + '\n')
