# Goals:
# 1. Get rid of first 20 data and last 20 data
# 2. Eliminate 10% too large and 10% too small values
import csv

# rawcsv = open("MPU6050.csv", 'r')
# procsv = open("MPU6050_filtered.csv", 'w')
rawcsv = open("MPU3300.csv", 'r')
procsv = open("MPU3300_filtered.csv", 'w')
headers = (["Sensor", "Axis", "Angular velocity", "X", "Y", "Z", "Temp"])
csvwriter = csv.DictWriter(procsv, headers)
csvwriter.writeheader()

# Set the filter rate, default value is 10%
filterRate = 0.1
previousAV = 0
previousAxis = 'X'
# One test period's data
onePeriod = []
csvDict = csv.DictReader(rawcsv)
for line in csvDict:
    if line["Angular velocity"] != previousAV:
        # Get rid of first 20 data and last 20 data
        onePeriod = onePeriod[20:-20]
        # Eliminate 10% too large and 10% too small values
        onePeriod = sorted(onePeriod, key=lambda x:x[previousAxis])
        filterNum = int(len(onePeriod) * filterRate)
        onePeriod = onePeriod[filterNum:-filterNum]
        csvwriter.writerows(onePeriod)
        previousAV = line["Angular velocity"]
        onePeriod = []
    else:
        onePeriod.append(line)

    if line["Axis"] != previousAxis:
        previousAxis = line["Axis"]

rawcsv.close()
procsv.close()