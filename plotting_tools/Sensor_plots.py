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
from matplotlib.dates import DateFormatter
from pytz import timezone
from datetime import datetime

SName = 'ElPanama', 'SanJuan', 'StationA', 'StationB'
myFmt = DateFormatter("%b")
# SName = 'ElPanama', 'ElCucero', 'SanJuan', 'StationA', 'StationB'
for StationName in SName:
    # Format the data
    #try:
    #    allSO2 = pd.read_csv('../data/' + StationName + '/allSO2.csv')
    #    allNO2 = pd.read_csv('../data/' + StationName + '/allNO2.csv')
    #except FileNotFoundError:
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
    plt.savefig('../plots/' + StationName + '/NO2' + time_p + '.png')


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
    plt.savefig('../plots/' + StationName + '/SO2' + time_p + '.png')


# El Panama
StationName = 'ElPanama'
allSO2 = pd.read_csv('../data/' + StationName + '/allSO2.csv')
allNO2 = pd.read_csv('../data/' + StationName + '/allNO2.csv')
T1s = ['2018-01-01 00:00:00', '2018-04-01 00:00:00',
       '2018-08-01 00:00:00', '2018-10-18 00:00:00']
T2s = ['2018-04-01 00:00:00', '2018-06-10 00:00:00',
       '2018-10-12 00:00:00', '2018-11-20 00:00:00']

TP = ['Jan2Apr', 'Apr2Jun', 'Jul2Oct', 'Recent']

for i in range(len(T1s)):
    plotterNO2(TP[i], T1s[i], T2s[i])
    plotterSO2(TP[i], T1s[i], T2s[i])

# SanJuan
StationName = 'SanJuan'
allSO2 = pd.read_csv('../data/' + StationName + '/allSO2.csv')
allNO2 = pd.read_csv('../data/' + StationName + '/allNO2.csv')
plotterNO2('Jan2Feb', '2018-01-01 00:00:00', '2018-02-01 00:00:00')
plotterSO2('Jan2Feb', '2018-01-01 00:00:00', '2018-02-01 00:00:00')

# StationA
StationName = 'StationA'
allSO2 = pd.read_csv('../data/' + StationName + '/allSO2.csv')
allNO2 = pd.read_csv('../data/' + StationName + '/allNO2.csv')
plotterNO2('Aug', '2018-07-01 00:00:00', '2018-09-01 00:00:00')
plotterSO2('Aug', '2018-07-01 00:00:00', '2018-09-01 00:00:00')

# StationB
StationName = 'StationB'
allSO2 = pd.read_csv('../data/' + StationName + '/allSO2.csv')
allNO2 = pd.read_csv('../data/' + StationName + '/allNO2.csv')
plotterNO2('Aug', '2018-07-01 00:00:00', '2018-09-01 00:00:00')
plotterSO2('Aug', '2018-07-01 00:00:00', '2018-09-01 00:00:00')

# bin the data
binLims = [0, 10, 350, 600, 2600, 9000, 14000]
bin_lables = ["vlow", "low", "moderate", "mod high", "high", "vhigh"]


def plotterSO2_binned(time_p, T1, T2):
    plt.figure(figsize=(15, 8))
    mask = ((allSO2['TBTimestamp'] > T1) &
            (allSO2['TBTimestamp'] <= T2))
    TPSO2 = allSO2.loc[mask]
    TPSO2.Scaled[TPSO2.Scaled < 0] = 0
    SO2bins = pd.cut(TPSO2.Scaled, binLims, labels=bin_lables)
    TPSO2.Scaled[SO2bins == 'vlow'] = 0
    TPSO2.Scaled[SO2bins == 'low'] = 10
    TPSO2.Scaled[SO2bins == 'moderate'] = 350
    TPSO2.Scaled[SO2bins == 'mod high'] = 600
    TPSO2.Scaled[SO2bins == 'high'] = 2600
    TPSO2.Scaled[SO2bins == 'vhigh'] = 9000
    ax = plt.gca()
    ax.set_title('SO$_{2}$ ' + time_p + ' 2018', fontsize=24)
    ax.set_yticks(binLims[1::])
    ax.set_yticklabels(bin_lables[1::])
    TPSO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.legend(['SO$_2$'], fontsize=18)
    # Remove axis label
    ax1 = plt.axes()
    ax1.xaxis.label.set_visible(False)
"""
from bokeh.models import ColumnDataSource
from bokeh.plotting import show, figure, output_file

output_file('test', title='Bokeh Plot', mode='cdn', root_dir=None)

def plotterSO2_binned(time_p, T1, T2):
    ax = figure(x_axis_type='datetime')
    mask = ((allSO2['TBTimestamp'] > T1) &
            (allSO2['TBTimestamp'] <= T2))
    TPSO2 = allSO2.loc[mask]
    TPSO2.Scaled[TPSO2.Scaled < 0] = 0
    SO2bins = pd.cut(TPSO2.Scaled, binLims, labels=bin_lables)
    TPSO2.Scaled[SO2bins == 'vlow'] = 0
    TPSO2.Scaled[SO2bins == 'low'] = 10
    TPSO2.Scaled[SO2bins == 'moderate'] = 350
    TPSO2.Scaled[SO2bins == 'mod high'] = 600
    TPSO2.Scaled[SO2bins == 'high'] = 2600
    TPSO2.Scaled[SO2bins == 'vhigh'] = 9000
    #ax.title('SO$_{2}$ ' + time_p + ' 2018', fontsize=24)
    #ax.set_yticks(binLims[1::])
    #ax.set_yticklabels(bin_lables[1::])
    source = ColumnDataSource(TPSO2)
    ax.line(x='TBTimestamp', y='Scaled', source=source)
    #ax.tick_params(axis='both', which='major', labelsize=18)
    #ax.legend(['SO$_2$'], fontsize=18)
    # Remove axis label
    #ax1 = plt.axes()
    #ax1.xaxis.label.set_visible(False)
    show(ax)
"""
