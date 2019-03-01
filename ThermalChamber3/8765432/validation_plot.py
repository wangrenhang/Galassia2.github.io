import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal

# Temperature profile and slices for each kind of sensors
temp = ["80", "70", "60", "50", "40", "30", "20"]
css = {"80": [18680, 25864], "70": [33048, 40839], "60": [48731, 55915],
       "50": [63301, 70687], "40": [77972, 85460], "30": [94162, 100233],
       "20": [107923, 115410]}
imgSlice = {"80": [18984, 24954], "70": [31734, 39323], "60": [48834, 54905],
       "50": [63607, 69779], "40": [78785, 84451], "30": [94367, 99325],
       "20": [107522, 114402]}
emgSlice ={"80": [19996, 25966], "70": [33656, 40536], "60": [47720, 55714],
      "50": [63301, 70385], "40": [77972, 85360], "30": [93455, 100133],
      "20": [107923, 115110]}
groSlice = {"80": [18680, 25864], "70": [34263, 40739], "60": [48731, 55715],
       "50": [64301, 70187], "40": [78177, 85360], "30": [93162, 100233],
       "20": [108523, 115110]}

# Process coarse sun sensors' voltage value to get bias under each temperature
def csuProcess(csu, t):
    # Slice raw data to derive clean data under each temperature
    csuloc = csu.loc[css[t][0]:css[t][1]]
    # csuloc.plot(title="Extracted css value at "+t+" ℃")
    # plt.xlabel("Data points")
    # plt.ylabel("Voltage / V")
    key = ["v1", "v2", "v3", "v4"]
    csumean = []
    for k in range(4):
        # Filter out the lamp effects and then use medium filter to clean data
        if t == "60":
            former = csuloc.iloc[:900, k].values
            latter = csuloc.iloc[1400:, k].values
            filtered = signal.medfilt(np.hstack((former, latter)), 5)
        else:
            filtered = signal.medfilt(csuloc.iloc[:, k].values, 5)
        # Visualize to see the performance
        plt.figure()
        plt.plot(filtered)
        plt.title('css'+str(k)+" under "+t+"℃")
        plt.xlabel("Data points")
        plt.ylabel("Voltage / V")
        # Calculate average bias
        csumean.append(np.mean(filtered))
    return csumean
#
# def cstProcess(cst, t):
#     # Slice raw data to derive clean data under each temperature
#     cstloc = cst.loc[css[t][0]:css[t][1]]
#     key = ["t1", "t2", "t3", "t4"]
#     cstmean = []
#     for k in key:
#         cstmean.append(np.mean(cstloc.loc[:, k].values))
#     return cstmean


# Use temperature value to get the indexes for slicing
# cst = pd.read_csv(r"CST.csv")
# cst.plot(title="Coarse sun sensor temperature")
# plt.xlabel("Data points")
# plt.ylabel("Temperature/℃")
# cstAvg = []
# for t in temp:
#     cstAvg.append(cstProcess(cst, t))
# print(cstAvg)
#
# Calibrate coarse sun sensor value
csu = pd.read_csv(r"CSV.csv")
# csu.plot(title="Coarse sun sensor value")
# plt.xlabel("Data points")
# plt.ylabel("Voltage/V")
csuAvg = []
for t in temp:
    csuAvg.append(csuProcess(csu, t))
print(csuAvg)


# def imgProcess(img, t):
#     # Slice raw data to derive clean data under each temperature
#     imgloc = img.loc[imgSlice[t][0]:imgSlice[t][1]]
#     imgloc.plot(title='Internal mag'+" under "+t+"℃")
#     plt.xlabel("Data points")
#     plt.ylabel("Magnetic field intensity / mG")
#     key = ["mx", "my", "mz"]
#     imgmean = []
#     for k in key:
#         imgmean.append(np.mean(imgloc.loc[:, k].values))
#     return imgmean

# img = pd.read_csv(r"IMG.csv")
# img.plot(y='mx', title='Internal mag x axis')
# plt.xlabel("Data points")
# plt.ylabel("Magnetic field intensity / mG")
# img.plot(y='my', title='Internal mag y axis')
# plt.xlabel("Data points")
# plt.ylabel("Magnetic field intensity / mG")
# img.plot(y='mz', title='Internal mag z axis')
# plt.xlabel("Data points")
# plt.ylabel("Magnetic field intensity / mG")
# imgAvg = []
# for t in temp:
#     imgAvg.append(imgProcess(img, t))
# print(imgAvg)


# def emgProcess(emg, t):
#     # Slice raw data to derive clean data under each temperature
#     emgloc = emg.loc[emgSlice[t][0]:emgSlice[t][1]]
#     emgloc.plot(y=["mx", "my", "mz"], title='External mag'+" under "+t+"℃")
#     plt.xlabel("Data points")
#     plt.ylabel("Magnetic field intensity / mG")
#     key = ["mx", "my", "mz"]
#     emgmean = []
#     for k in key:
#         emgmean.append(np.mean(emgloc.loc[:, k].values))
#     return emgmean

# emg = pd.read_csv(r"EMG.csv")
# emg.plot(y='mx', title='External mag x axis')
# plt.xlabel("Data points")
# plt.ylabel("Magnetic field intensity / mG")
# emg.plot(y='my', title='External mag y axis')
# plt.xlabel("Data points")
# plt.ylabel("Magnetic field intensity / mG")
# emg.plot(y='mz', title='External mag z axis')
# plt.xlabel("Data points")
# plt.ylabel("Magnetic field intensity / mG")
# emg.plot(y='temp', title='External mag temp')
# plt.xlabel("Data points")
# plt.ylabel("Temperature given by A3200 / ℃")
# emgAvg = []
# for t in temp:
#     emgAvg.append(emgProcess(emg, t))
# print(emgAvg)


# def groProcess(gro, t):
#     # Slice raw data to derive clean data under each temperature
#     groloc = gro.loc[groSlice[t][0]:groSlice[t][1]]
#     groloc.plot(y = ['x', 'y', 'z'], title='Gyroscope'+" under "+t+"℃")
#     plt.xlabel("Data points")
#     plt.ylabel("Angular velocity / (rad/s)")
#     key = ["x", "y", "z", "temp"]
#     gromean = []
#     for k in key:
#         gromean.append(np.mean(groloc.loc[:, k].values))
#     return gromean

# gro = pd.read_csv(r"GRO.csv")
# gro.plot(y='x', title='Gyro x axis value')
# plt.xlabel("Data points")
# plt.ylabel("Angular velocity / (rad/s)")
# gro.plot(y='y', title='Gyro y axis value')
# plt.xlabel("Data points")
# plt.ylabel("Angular velocity / (rad/s)")
# gro.plot(y='z', title='Gyro z axis value')
# plt.xlabel("Data points")
# plt.ylabel("Angular velocity / (rad/s)")
# gro.plot(y='temp', title='Gyro temperature')
# plt.xlabel("Data points")
# plt.ylabel("Temperature / ℃")
# groAvg = []
# for t in temp:
#     groAvg.append(groProcess(gro, t))
# print(groAvg)

plt.show()

