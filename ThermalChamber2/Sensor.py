class SDPlt:

    def __init__(self, name, ):

        # Fine sun sensor visualization
        if data[0] == "FSS":

            # Fine sun sensor's data is incomplete if its length is less than 4
            if len(data) != 4:
                continue

            try:
                for i in range(len(data)):
                    if i == 0:
                        continue
                    else:
                        data[i] = float(data[i])
            except ValueError:
                continue

            # Write to CSV file
            fss.writerow(data[1:])

            fssFig = plt.figure(1)
            fssFig.suptitle("Fine sun sensor", fontsize=16)

            fssThetaFig = plt.subplot(131)
            fssThetaFig.set_title("Theta")
            plt.xlim([fssCnt * 100, fssCnt * 100 + 100])
            plt.ylim([-2, 8])
            fssTheta.append(data[1])
            plt.plot(range(fssCnt * 100, fssCnt * 100 + 100)[:len(fssTheta)], fssTheta)  # 将list传入plot画图

            fssPhiFig = plt.subplot(132)
            fssPhiFig.set_title("Phi")
            plt.xlim([fssCnt * 100, fssCnt * 100 + 100])
            plt.ylim([-2, 8])
            fssPhi.append(data[2])
            plt.plot(range(fssCnt * 100, fssCnt * 100 + 100)[:len(fssPhi)], fssPhi)  # 将list传入plot画图

            fssTfig = plt.subplot(133)
            fssTfig.set_title("Temperature")
            plt.xlim([fssCnt * 100, fssCnt * 100 + 100])
            plt.ylim([-150, 150])
            fssT.append(data[3])
            plt.plot(range(fssCnt * 100, fssCnt * 100 + 100)[:len(fssT)], fssT)  # 将list传入plot画图

            plt.pause(0.001)  # 这个为停顿0.01s，能得到产生实时的效果

            if len(fssT) >= 100:
                fssTheta = []
                fssPhi = []
                fssT = []
                plt.clf()
                fssCnt = fssCnt + 1