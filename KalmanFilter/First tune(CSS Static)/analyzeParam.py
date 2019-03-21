import pandas as pd
import numpy as np

def main():
    euler = pd.read_csv("euler.csv")
    eukal = pd.read_csv("eukal.csv")

    kalYaw = eukal["yaw"]
    kalp1 = eukal["p1"]
    kalp2 = eukal["p2"]
    kalp3 = eukal["p3"]
    kalp4 = eukal["p4"]

    length = len(kalYaw)
    yawTemp = []
    pTemp = [kalp1[0], kalp2[0], kalp3[0], kalp4[0]]
    table = {}
    for i in range(length):
        if pTemp == [kalp1[i], kalp2[i], kalp3[i], kalp4[i]]:
            yawTemp.append(kalYaw[i])
        else:
            table[str(pTemp)] = [np.mean(yawTemp), np.var(yawTemp)]
            yawTemp = []
            pTemp = [kalp1[i], kalp2[i], kalp3[i], kalp4[i]]
            yawTemp.append(kalYaw[i])

    print(table)
    table = sorted(table.items(), key=lambda item:item[1])
    # CSS + Static best 20 parameters
    for i in range(20):
        print(table[i][0])


if __name__ == "__main__":
    main()