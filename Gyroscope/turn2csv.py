import csv

# rawFile = open("MPU6050.txt", 'r')
# csvFile = open("MPU6050.csv", 'w')
rawFile = open("MPU6050_validation.txt", 'r')
csvFile = open("MPU6050_validation.csv", 'w')

writer = csv.writer(csvFile)
# Write header first
writer.writerow(["Sensor", "Axis", "Angular velocity", "X", "Y", "Z", "Temp"])

# Write row by row
# Raw data style:
# X0 b'EXT: x = -0.595093, y = -0.114441, z = -1.205444, temp = 25.330000\r\n'
while True:
    line = rawFile.readline()
    line = str(line)
    # Eliminate polluted data
    if line == '':
        break
    if line.find("temp = ") == -1:
        continue

    csvLine = []
    # Add sensor type
    if line.find("EXT") != -1:
        csvLine.append("EXT")
    elif line.find("E33") != -1:
        csvLine.append("E33")
    elif line.find("INT") != -1:
        csvLine.append("INT")
    elif line.find("Kal") != -1:
        csvLine.append("Kal")
    else:
        continue

    # Add axis
    if line.startswith("X"):
        csvLine.append("X")
    elif line.startswith("Y"):
        csvLine.append("Y")
    elif line.startswith("Z"):
        csvLine.append("Z")
    else:
        continue

    # Add standard angular velocity
    avIndex = line.find(' ')
    if avIndex == -1:
        continue
    csvLine.append(line[1:avIndex])

    # Add measured data
    xIndex = line.find("x = ")
    yIndex = line.find("y = ")
    zIndex = line.find("z = ")
    tIndex = line.find("temp = ")
    eIndex = line.find("\\r\\n")
    csvLine.append(float(line[xIndex + 4:yIndex - 2]))
    csvLine.append(float(line[yIndex + 4:zIndex - 2]))
    csvLine.append(float(line[zIndex + 4:tIndex - 2]))
    csvLine.append(float(line[tIndex + 7:eIndex]))

    writer.writerow(csvLine)


writer.writerow(["EXT",'E',0,0,0,0,0])
rawFile.close()
csvFile.close()
