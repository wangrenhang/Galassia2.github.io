import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal

# Temperature profile and slices for each kind of sensors
temp = ["20", "10", "0", "-10", "-20", "-30"]
css = {"20": [3503, 7679], "10": [13702, 22456], "0": [30005, 37310],
       "-10": [44942, 51848], "-20": [61485, 67107], "-30": [74495, 81402]}
imgSlice = {"20": [4071, 7588], "10": [15176, 21284], "0": [29798, 35721],
            "-10": [45160, 50343], "-20": [61263, 66075], "-30": [73848, 80141]}
emgSlice = {"20": [3701, 6848], "10": [16842, 22025], "0": [32945, 36831],
            "-10": [46641, 51400], "-20": [61448, 66445], "-30": [75884, 81067]}
groSlice = {"20": [4226, 7598], "10": [14906, 22455], "0": [30964, 36909],
            "-10": [45101, 51926], "-20": [58993, 66943], "-30": [74412, 81318]}

# # Process coarse sun sensors' voltage value to get bias under each temperature
# def csuProcess(csu, t):
#     # Slice raw data to derive clean data under each temperature
#     csuloc = csu.loc[css[t][0]:css[t][1]]
#     # csuloc.plot(title="Extracted css value at "+t+" ℃")
#     # plt.xlabel("Data points")
#     # plt.ylabel("Voltage / V")
#     key = ["v1", "v2", "v3", "v4"]
#     csumean = []
#     for k in range(4):
#         # Filter out the lamp effects and then use medium filter to clean data
#         if t == "-30":
#             former = csuloc.iloc[:3000, k].values
#             latter = csuloc.iloc[3200:, k].values
#             filtered = signal.medfilt(np.hstack((former, latter)), 5)
#         else:
#             filtered = signal.medfilt(csuloc.iloc[:, k].values, 5)
#         # # Visualize to see the performance
#         # plt.figure()
#         # plt.plot(filtered)
#         # plt.title('css'+str(k)+" under "+t+"℃")
#         # plt.xlabel("Data points")
#         # plt.ylabel("Voltage / V")
#         # Calculate average bias
#         csumean.append(np.mean(filtered))
#     return csumean
#
# def cstProcess(cst, t):
#     # Slice raw data to derive clean data under each temperature
#     cstloc = cst.loc[css[t][0]:css[t][1]]
#     key = ["t1", "t2", "t3", "t4"]
#     cstmean = []
#     for k in key:
#         cstmean.append(np.mean(cstloc.loc[:, k].values))
#     return cstmean


# # Use temperature value to get the indexes for slicing
# cst = pd.read_csv(r"CST.csv")
# # cst.plot(title="Coarse sun sensor temperature")
# # plt.xlabel("Data points")
# # plt.ylabel("Temperature/℃")
# cstAvg = []
# for t in temp:
#     cstAvg.append(cstProcess(cst, t))
# print(cstAvg)
#
# # Calibrate coarse sun sensor value
# csu = pd.read_csv(r"CSV.csv")
# # csu.plot(title="Coarse sun sensor value")
# # plt.xlabel("Data points")
# # plt.ylabel("Voltage/V")
# csuAvg = []
# for t in temp:
#     csuAvg.append(csuProcess(csu, t))
# print(csuAvg)


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
#     emgloc.plot(title='External mag'+" under "+t+"℃")
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


def groProcess(gro, t):
    # Slice raw data to derive clean data under each temperature
    groloc = gro.loc[groSlice[t][0]:groSlice[t][1]]
    groloc.plot(y = ['x', 'y', 'z'], title='Gyroscope'+" under "+t+"℃")
    plt.xlabel("Data points")
    plt.ylabel("Angular velocity / (rad/s)")
    key = ["x", "y", "z", "temp"]
    gromean = []
    for k in key:
        gromean.append(np.mean(groloc.loc[:, k].values))
    return gromean

gro = pd.read_csv(r"GRO.csv")
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
groAvg = []
for t in temp:
    groAvg.append(groProcess(gro, t))
print(groAvg)

plt.show()

