# -*- coding: utf-8 -*-
"""Sensor Plotter

This module was developed by CEMAC as part of the UNRESP Project.
This script takes data from the AQ Sensors (obtained by getAQMeshData.py)
and plots the data - Any found from all stations

Example:
    To use::

Attributes:

.. CEMAC_stomtracking:
   https://github.com/cemac/UNRESP_AQSensorTools
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from pytz import timezone
from datetime import datetime

SName = ["SanJu1", "ElCrucero", "SanJuan2", "785150", "Pacaya", "Rigoberto",
         "861150", "Met", "ElPanama"]
myFmt = DateFormatter("%Y %b ")
for StationName in SName:
    example = pd.read_csv('../data/ElPanama/AQMeshData_1733150_2018-01-01T00' +
                          '-00-00_to_2018-12-03T09-59-10_SO2-NO2.csv')
    pname = '../data/' + StationName + '/AQMeshData*.csv'
    for rw in glob.iglob(pname):
        day_data = pd.read_csv(rw)
        NO2 = day_data[day_data.SensorLabel == 'NO2']
        SO2 = day_data[day_data.SensorLabel != 'NO2']
        NO2_valid = NO2[NO2.Status == 'Valid']
        SO2_valid = SO2[SO2.Status == 'Valid']
        allSO2 = SO2_valid.reset_index(drop=True)
        allNO2 = NO2_valid.reset_index(drop=True)

    allNO2['TBTimestamp'] = pd.to_datetime(allNO2['TBTimestamp'])
    allSO2['TBTimestamp'] = pd.to_datetime(allSO2['TBTimestamp'])
    allNO2['TBTimestamp'].apply(lambda x: datetime.replace(x, tzinfo=None))
    allSO2['TBTimestamp'].apply(lambda x: datetime.replace(x, tzinfo=None))
    allNO2['date'] = allNO2['TBTimestamp'].apply(lambda x: x.strftime("%Y %b"))
    allSO2['date'] = allSO2['TBTimestamp'].apply(lambda x: x.strftime("%Y %b"))
    print('../data/' + StationName + '/allSO2.csv')
    allSO2.to_csv('../data/' + StationName + '/allSO2.csv', sep=',')
    allNO2.to_csv('../data/' + StationName + '/allNO2.csv', sep=',')

    # plot whole dataset
    T1 = datetime(2018, 1, 1, 0, 0, 0).replace(tzinfo=None)
    T2 = datetime(2018, 12, 1, 0, 0, 0).replace(tzinfo=None)
    plt.figure(figsize=(100, 8))
    ax = plt.gca()
    ax.set_title(r'NO$_2$ 2018', fontsize=48)
    if not allNO2.empty:
        allNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
        ax.set_xlim([T1, T2])
        ax.tick_params(axis='both', which='major', labelsize=48)
        ax.xaxis.set_major_formatter(myFmt)
        ax.xaxis_date()
        plt.savefig('../plots/' + StationName + '/NO22018.png')
        plt.figure(figsize=(100, 8))
        ax = plt.gca()
    if allSO2.empty:
        continue
    ax.set_title(r'SO$_2$ 2018', fontsize=48)
    allSO2.plot.line(x='TBTimestamp', y='Scaled', color='red', ax=ax)
    ax.set_xlim([T1, T2])
    ax.tick_params(axis='both', which='major', labelsize=48)
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis_date()
    plt.savefig('../plots/' + StationName + '/SO22018.png')
