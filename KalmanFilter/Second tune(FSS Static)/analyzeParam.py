import pandas as pd
import numpy as np

def analyze(table, eukal):
    kalYaw = eukal["yaw"]
    kalp1 = eukal["p1"]
    kalp2 = eukal["p2"]
    kalp3 = eukal["p3"]
    kalp4 = eukal["p4"]

    length = len(kalYaw)
    yawTemp = []
    pTemp = [kalp1[0], kalp2[0], kalp3[0], kalp4[0]]
    for i in range(length):
        if pTemp == [kalp1[i], kalp2[i], kalp3[i], kalp4[i]]:
            yawTemp.append(kalYaw[i])
        else:
            table[str(pTemp)] = [np.mean(yawTemp), np.var(yawTemp)]
            yawTemp = []
            pTemp = [kalp1[i], kalp2[i], kalp3[i], kalp4[i]]
            yawTemp.append(kalYaw[i])
    return table

def main():
    euler = pd.read_csv("euler.csv")
    eukal = pd.read_csv("eukal.csv")

    rawTable = {}
    kalTable = {}

    rawTable = analyze(rawTable, euler)
    kalTable = analyze(kalTable, eukal)

    kalTable = sorted(kalTable.items(), key=lambda item:item[1])
    # CSS + Static best 10 parameters
    for i in range(10):
        good = kalTable[i]
        print(good)
        goodKey = good[0]
        print(rawTable[goodKey])


if __name__ == "__main__":
    main()