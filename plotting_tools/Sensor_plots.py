# -*- coding: utf-8 -*-
"""Sensor Plotter

This module was developed by CEMAC as part of the UNRESP Project.
This script takes data from the AQ Sensors (obtained by getAQMeshData.py)
and plots the data.

Example:
    To use::

Attributes:

.. CEMAC_stomtracking:
   https://github.com/cemac/UNRESP_AQSensorTools
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt


pname = '../data/*'
for rw in glob.iglob(pname):
    day_data = pd.read_csv(rw)
    NO2 = day_data[day_data.SensorLabel == 'NO2']
    SO2 = day_data[day_data.SensorLabel != 'NO2']
    NO2_valid = NO2[NO2.Status == 'Valid']
    SO2_valid = SO2[SO2.Status == 'Valid']
    allSO2 = pd.concat([allSO2, SO2_valid]).reset_index(drop=True)
    allNO2 = pd.concat([allNO2, NO2_valid]).reset_index(drop=True)

allNO2['TBTimestamp'] = pd.to_datetime(allNO2['TBTimestamp'])
allSO2['TBTimestamp'] = pd.to_datetime(allSO2['TBTimestamp'])

# plot whole dataset
plt.figure(figsize=(100, 8))
ax = plt.gca()
ax.set_title('../plots/NO2 2018', fontsize=18)
allNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
plt.savefig('NO22018.png')
plt.figure(figsize=(100, 8))
ax = plt.gca()
allSO2.plot.line(x='TBTimestamp', y='Scaled', color='red', ax=ax)
plt.savefig('../plots/SO22018.png')


def plotterNO2(time_p, T1, T2):
    plt.figure(figsize=(15, 8))
    mask = ((allNO2['TBTimestamp'] > T1) &
            (allNO2['TBTimestamp'] <= T2))
    TPNO2 = allNO2.loc[mask]
    ax = plt.gca()
    ax.set_title('NO$_{2}$ ' + time_p + ' 2018', fontsize=24)
    ax.set_ylabel(' (ppb) ', fontsize=20)
    TPNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.legend(['NO$_2$'], fontsize=18)
    # Remove axis label
    ax1 = plt.axes()
    ax1.xaxis.label.set_visible(False)
    plt.savefig('../plots/NO2' + time_p + '.png')


def plotterSO2(time_p, T1, T2):
    plt.figure(figsize=(15, 8))
    mask = ((allSO2['TBTimestamp'] > T1) &
            (allSO2['TBTimestamp'] <= T2))
    TPSO2 = allSO2.loc[mask]
    ax = plt.gca()
    ax.set_title('SO$_{2}$ ' + time_p + ' 2018', fontsize=24)
    ax.set_ylabel(' (ppb) ', fontsize=20)
    TPSO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.legend(['SO$_2$'], fontsize=18)
    # Remove axis label
    ax1 = plt.axes()
    ax1.xaxis.label.set_visible(False)
    plt.savefig('../plots/SO2' + time_p + '.png')


T1s = ['2018-01-01 00:00:00', '2018-04-01 00:00:00',
       '2018-08-01 00:00:00', '2018-10-18 00:00:00']
T2s = ['2018-04-01 00:00:00', '2018-06-10 00:00:00',
       '2018-10-12 00:00:00', '2018-11-20 00:00:00']

TP = ['Jan2Apr', 'Apr2Jun', 'Jul2Oct', 'Recent']

for i in range(len(T1s)):
    plotterNO2(TP[i], T1s[i], T2s[i])
    plotterSO2(TP[i], T1s[i], T2s[i])
