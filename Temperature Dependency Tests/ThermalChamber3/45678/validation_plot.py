import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.signal as signal

# Temperature profile and slices for each kind of sensors
temp = ["40", "50", "60", "70", "80"]
css = {"40": [3476, 9639], "50": [16704, 24109], "60": [32474, 39193],
       "70": [47421, 54003], "80": [61409, 68539]}
imgSlice = {"40": [4911, 8134], "50": [18076, 23424], "60": [32544, 37755],
            "70": [47424, 53183], "80": [62372, 67172]}
emgSlice = {"40": [3402, 9985], "50": [18007, 24796], "60": [33641, 39538],
            "70": [48589, 54212], "80": [64086, 68886]}
groSlice = {"40": [4225, 9985], "50": [17459, 24042], "60": [32474, 38784],
            "70": [49138, 54007], "80": [61961, 68887]}

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
        if t == "70":
            former = csuloc.iloc[:900, k].values
            latter = csuloc.iloc[1400:, k].values
            filtered = signal.medfilt(np.hstack((former, latter)), 5)
        elif t == "80":
            s1 = csuloc.iloc[:2458, k].values
            s2 = csuloc.iloc[2758:5448, k].values
            s3 = csuloc.iloc[5635:6935, k].values
            s = np.hstack((s1, s2, s3))
            filtered = signal.medfilt(s, 5)

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
# # cst.plot(title="Coarse sun sensor temperature")
# # plt.xlabel("Data points")
# # plt.ylabel("Temperature/℃")
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
#
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
#
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

