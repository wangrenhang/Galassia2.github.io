import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze(table, eukal):
    rawYaw = eukal["raw yaw"]
    kalYaw = eukal["kal yaw"]
    kalp1 = eukal["p1"]
    kalp2 = eukal["p2"]
    kalp3 = eukal["p3"]
    kalp4 = eukal["p4"]

    length = len(kalYaw)
    rawyawTemp = []
    kalyawTemp = []
    pTemp = [kalp1[0], kalp2[0], kalp3[0], kalp4[0]]
    for i in range(length):
        if pTemp == [kalp1[i], kalp2[i], kalp3[i], kalp4[i]]:
            # yawTemp.append(np.fabs(kalYaw[i]-rawYaw[i]))
            rawyawTemp.append(rawYaw[i])
            kalyawTemp.append(kalYaw[i])
        else:
            # table[str(pTemp)] = [np.mean(yawTemp), np.var(yawTemp)]
            plt.figure()
            l1, = plt.plot(rawyawTemp, 'b')
            l2, = plt.plot(kalyawTemp, 'r')
            rawyawTemp = []
            kalyawTemp = []
            pTemp = [kalp1[i], kalp2[i], kalp3[i], kalp4[i]]
            rawyawTemp.append(rawYaw[i])
            kalyawTemp.append(kalYaw[i])
    return table

def main():
    euler = pd.read_csv("euler.csv")

    rawTable = {}

    rawTable = analyze(rawTable, euler)

    for t in rawTable.keys():
        print(rawTable[t])

    # optimRate = []
    # for k in rawTable.keys():
    #     rawVar = rawTable[k][1]
    #     kalVar = kalTable[k][1]
    #     if rawVar <= kalVar:
    #         continue
    #     optimRate.append([k, (rawVar-kalVar)/rawVar])
    #
    # res = sorted(optimRate, key=lambda item: item[1], reverse=True)
    # for i in range(6):
    #     good = res[i]
    #     print(good[0])
    #     # goodKey = good[0]
    #     # print(rawTable[goodKey])
    #     # print(kalTable[goodKey])

    plt.show()


if __name__ == "__main__":
    main()