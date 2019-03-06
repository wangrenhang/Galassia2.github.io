import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd

# b'FSS: 0.000000 0.000000 20.250000\r\n'
# b'CST: 20.653532 20.573059 20.637436 20.621349\r\n'
# b'CSV: 0.014438 0.014813 0.014813 0.014438\r\n'
# b'IMG: -524.359009 6.410256 -74.358978\r\n'
# b'EMG: 373.466675 -197.733322 51.466667 33.843750\r\n'
# b'GRO: 0.195706 0.552795 -0.014072 19.912354\r\n'

# fss = pd.read_csv(r"FSS.csv")
# fss.dropna(axis=0, how='any')
# for i in range(fss.index.max()):
#     if any([fss.loc[i, 'temp'] > 100.0 or fss.loc[i, 'temp'] < -50,
#             fss.loc[i, 'theta'] > 10 or fss.loc[i, 'theta'] < -1,
#             fss.loc[i, 'phi'] > 10 or fss.loc[i, 'phi'] < -1]):
#         fss.drop([i], inplace=True)
# fss.plot(y='temp', title='FSS temperature')
# fss.plot(kind='hist', y='theta', title='FSS theta value')
# fss.plot(kind='hist', y='phi', title='FSS phi value')
#
# cst = pd.read_csv(r"CST.csv")
# cst.dropna(axis=0, how='any')
# for i in range(cst.index.max()):
#     if any([cst.loc[i, 't1'] > 100,
#             cst.loc[i, 't2'] > 100,
#             cst.loc[i, 't3'] > 100,
#             cst.loc[i, 't4'] > 100]):
#         cst.drop([i], inplace=True)
# cst.plot()
#
csu = pd.read_csv(r"CSV.csv")
csu.dropna(axis=0, how='any')
for i in range(csu.index.max()):
    if any([csu.loc[i, 'v1'] > 100,
            csu.loc[i, 'v2'] > 100,
            csu.loc[i, 'v3'] > 100,
            csu.loc[i, 'v4'] > 100]):
        csu.drop([i], inplace=True)
csu.plot()

# img = pd.read_csv(r"IMG.csv")
# img.dropna(axis=0, how='any')
# for i in range(img.index.max()):
#     if any([img.loc[i, 'm1'] > 1000 or img.loc[i, 'm1'] < -1000,
#             img.loc[i, 'm2'] > 1000 or img.loc[i, 'm2'] < -1000,
#             img.loc[i, 'm3'] > 1000 or img.loc[i, 'm3'] < -1000]):
#         img.drop([i], inplace=True)
# img.plot()
#
emg = pd.read_csv(r"EMG.csv")
emg.dropna(axis=0, how='any')
for i in range(emg.index.max()):
    if any([emg.loc[i, 'm1'] > 1000 or emg.loc[i, 'm1'] < -1000,
            emg.loc[i, 'm2'] > 1000 or emg.loc[i, 'm2'] < -1000,
            emg.loc[i, 'm3'] > 1000 or emg.loc[i, 'm3'] < -1000,
            emg.loc[i, 'temp'] > 50 or emg.loc[i, 'temp'] < -40]):
        emg.drop([i], inplace=True)
# emg.plot(y=['m1', 'm2', 'm3'], title='External mag value')
emg.plot(y='temp', title='External mag temperature')
#
# gro = pd.read_csv(r"GRO.csv")
# gro.dropna(axis=0, how='any')
# for i in range(gro.index.max()):
#     if any([gro.loc[i, 'x'] > 2 or gro.loc[i, 'x'] < -2,
#             gro.loc[i, 'y'] > 2 or gro.loc[i, 'y'] < -2,
#             gro.loc[i, 'z'] > 2 or gro.loc[i, 'z'] < -2,
#             gro.loc[i, 'temp'] > 100 or gro.loc[i, 'temp'] < -100]):
#         gro.drop([i], inplace=True)
# gro.plot(y=['x', 'y', 'z'], title='Gyro value')
# gro.plot(y='x', title='Gyro x axis value')
# gro.plot(y='y', title='Gyro y axis value')
# gro.plot(y='z', title='Gyro z axis value')
# gro.plot(y='temp', title='Gyro temperature')

plt.show()


