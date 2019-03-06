import csv

counter = 0
err = 0

rawFile = open("ThermalChamber.txt", 'r')
fssFile = open("FSS.csv", 'w')
cstFile = open("CST.csv", 'w')
csvFile = open("CSV.csv", 'w')
imgFile = open("IMG.csv", 'w')
emgFile = open("EMG.csv", 'w')
groFile = open("GRO.csv", 'w')

fss = csv.writer(fssFile)
cst = csv.writer(cstFile)
csu = csv.writer(csvFile)
img = csv.writer(imgFile)
emg = csv.writer(emgFile)
gro = csv.writer(groFile)

# Write header first
fss.writerow(["theta", "phi", "temp"])
cst.writerow(["t1", "t2", "t3", "t4"])
csu.writerow(["v1", "v2", "v3", "v4"])
img.writerow(["m1", "m2", "m3"])
emg.writerow(["m1", "m2", "m3", "temp"])
gro.writerow(["x", "y", "z", "temp"])


def extract(writer, dat, n):
    global err
    csvLine = []
    test = dat

    for i in range(n):
        index = dat.find(' ')
        if index == -1:
            return
        try:
            csvLine.append(float(dat[:index]))
        except ValueError:
            return
        dat = dat[index+1:]

    index = dat.find('\\r')
    if index == -1:
        return

    try:
        csvLine.append(float(dat[:index]))
    except ValueError:
        return

    if csvLine[0] < -1000 or csvLine[0] > 1000 or csvLine[1] < -1000 or csvLine[1] > 1000:
        print(str(counter)+" "+test)
        err += 1

    writer.writerow(csvLine)

# Write row by row
# Raw data style:
# b'FSS: 0.000000 0.000000 20.250000\r\n'
# b'CST: 20.653532 20.573059 20.637436 20.621349\r\n'
# b'CSV: 0.014438 0.014813 0.014813 0.014438\r\n'
# b'IMG: -524.359009 6.410256 -74.358978\r\n'
# b'EMG: 373.466675 -197.733322 51.466667 33.843750\r\n'
# b'GRO: 0.195706 0.552795 -0.014072 19.912354\r\n'
while True:

    counter = counter + 1

    line = rawFile.readline()
    line = str(line)
    # Eliminate polluted data
    if line == '':
        break
    firstSpace = line.find(': ')
    if firstSpace == -1:
        continue
    endSymbol = line.find('\\r\\n')
    if endSymbol == -1:
        continue
    cntSpace = line.count(' ', firstSpace+2, endSymbol)
    # print(cntSpace)

    if line.find("FSS: ") != -1:
        if cntSpace != 2:
            continue
        else:
            extract(fss, line[firstSpace+2:], cntSpace)

    elif line.find("CST: ") != -1:
        if cntSpace != 3:
            continue
        else:
            extract(cst, line[firstSpace+2:], cntSpace)

    elif line.find("CSV: ") != -1:
        if cntSpace != 3:
            continue
        else:
            extract(csu, line[firstSpace+2:], cntSpace)

    elif line.find("IMG: ") != -1:
        if cntSpace != 2:
            continue
        else:
            extract(img, line[firstSpace+2:], cntSpace)

    elif line.find("EMG: ") != -1:
        if cntSpace != 3:
            continue
        else:
            extract(emg, line[firstSpace+2:], cntSpace)

    elif line.find("GRO: ") != -1:
        if cntSpace != 3:
            continue
        else:
            extract(gro, line[firstSpace+2:], cntSpace)

    else:
        continue

# fss.writerow(['E', 'E', 'E'])
# cst.writerow(['E', 'E', 'E', 'E'])
# csu.writerow(['E', 'E', 'E', 'E'])
# img.writerow(['E', 'E', 'E'])
# emg.writerow(['E', 'E', 'E', 'E'])
# gro.writerow(['E', 'E', 'E', 'E'])
rawFile.close()
fssFile.close()
cstFile.close()
csvFile.close()
imgFile.close()
emgFile.close()
groFile.close()

print(err)
