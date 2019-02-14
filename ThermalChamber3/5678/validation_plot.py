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

fss = pd.read_csv(r"FSS.csv")
fss.plot(y='temp', title='FSS temperature', subplots=True)
fss.plot(y='theta', title='FSS theta value', subplots=True)
fss.plot(y='phi', title='FSS phi value', subplots=True)


cst = pd.read_csv(r"CST.csv")
cst.plot()

csu = pd.read_csv(r"CSV.csv")
csu.plot(y='v1', title='CSS 1')
csu.plot(y='v2', title='CSS 2')
csu.plot(y='v3', title='CSS 3')
csu.plot(y='v4', title='CSS 4')

img = pd.read_csv(r"IMG.csv")
img.plot()

emg = pd.read_csv(r"EMG.csv")
emg.plot(y=['mx', 'my', 'mz'], title='External mag value')
emg.plot(y='temp', title='External mag temperature')

gro = pd.read_csv(r"GRO.csv")
gro.plot(y=['x', 'y', 'z'], title='Gyro value')
gro.plot(y='x', title='Gyro x axis value')
gro.plot(y='y', title='Gyro y axis value')
gro.plot(y='z', title='Gyro z axis value')
gro.plot(y='temp', title='Gyro temperature')

plt.show()


