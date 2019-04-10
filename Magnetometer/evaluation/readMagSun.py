import serial
import csv

# Choose one sensor to show its output
sensorToShow = 6

def dataExtract(data):

    name = ["Sun Vec", "Mag Vec", "Euler"]

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

def main():

    # Open serial port to read raw data
    srl = serial.Serial('com3', 38400)

    # Open CSV files
    sunFile = open("SUN.csv", 'w')
    magFile = open("MAG.csv", 'w')
    eulFile = open("EULER.csv", 'w')

    # Initial CSV writers
    sun = csv.writer(sunFile)
    mag = csv.writer(magFile)
    eul = csv.writer(eulFile)

    # Write CSV header first
    sun.writerow(["x", "y", "z"])
    mag.writerow(["x", "y", "z"])
    eul.writerow(["raw", "kal"])

    sunFile.close()
    magFile.close()
    eulFile.close()

    while True:

        data = srl.readline()
        data = str(data)

        # Do data cleaning, eliminate incomplete lines but reserve corrupted data for further analyzing
        # Extract useful information from the cleaned raw input data
        data = dataExtract(data)
        if data == -1:
            continue
        print(data)

        # Sun vector
        if data[0] == "Sun Vec":

            # Sun vector's data is incomplete if its length is less than 3
            if len(data) != 3:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            with open("SUN.csv", 'a') as sunFile:
                sun = csv.writer(sunFile)
                sun.writerow(data[1:])

        # Mag vector
        elif data[0] == "Mag Vec":

            # Mag vector's data is incomplete if its length is less than 3
            if len(data) != 3:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            with open("MAG.csv", 'a') as magFile:
                mag = csv.writer(magFile)
                mag.writerow(data[1:])

        # Euler angle
        elif data[0] == "Euler":

            # Euler angle's data is incomplete if its length is less than 3
            if len(data) != 3:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            with open("EULER.csv", 'a') as eulFile:
                eul = csv.writer(eulFile)
                eul.writerow(data[1:])

        else:
            continue


if __name__ == "__main__":
    main()