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

SName = ["SanJu1", "ElCrucero", "SanJuan2", "785150", "Pacaya", "Rigoberto",
         "861150", "Met", "ElPanama"]
myFmt = DateFormatter("%Y %b ")
myFmtday = DateFormatter("%d ")


def plotTSNO2(StationName, month=1, year=2016, ymax=100):
    pname = '../data/' + StationName + '/AQMeshData*_2016*.csv'
    for rw in glob.iglob(pname):
        day_data = pd.read_csv(rw)
        NO2 = day_data[day_data.SensorLabel == 'NO2']
        SO2 = day_data[day_data.SensorLabel == 'SO2']
        NO2_valid = NO2[NO2.Status == 'Valid']
        SO2_valid = SO2[SO2.Status == 'Valid']
        allNO2 = NO2_valid.reset_index(drop=True)
        allSO2 = SO2_valid.reset_index(drop=True)
    allNO2['TBTimestamp'] = pd.to_datetime(allNO2['TBTimestamp'])
    allNO2['TBTimestamp'].apply(lambda x: datetime.replace(x, tzinfo=None))
    allNO2['date'] = allNO2['TBTimestamp'].apply(lambda x: x.strftime("%Y %b"))
    allSO2['TBTimestamp'] = pd.to_datetime(allNO2['TBTimestamp'])
    allSO2['TBTimestamp'].apply(lambda x: datetime.replace(x, tzinfo=None))
    allSO2['date'] = allSO2['TBTimestamp'].apply(lambda x: x.strftime("%Y %b"))
    T1 = datetime(year, month, 1, 0, 0, 0).replace(tzinfo=None)
    if month == 12:
        T2 = datetime(year, month, 31, 0, 0, 0).replace(tzinfo=None)
    else:
        T2 = datetime(year, month + 1, 1, 0, 0, 0).replace(tzinfo=None)
    plt.figure(figsize=(30, 10))
    ax = plt.gca()
    ax.set_title(StationName + r' NO$_2$ and SO$_2$' + '\n', fontsize=48)
    if not allNO2.empty:
        allNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax, color='b')
        ax.set_xlim([T1, T2])
        ax.set_ylabel('NO$_2$', fontsize=48, color='b')
        ax.tick_params(axis='both', which='major', labelsize=48)
        ax.tick_params(axis='y', which='major', labelsize=48, colors='b')
        ax.xaxis.set_major_formatter(myFmtday)
        ax.xaxis_date()
        ax.set_xlabel(T1.strftime('%b %Y'), fontsize=48)
        ax2 = ax.twinx()
        allSO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax2, color='g')
        ax2.set_xlim([T1, T2])
        ax2.xaxis_date()
        ax2.xaxis.set_major_formatter(myFmtday)
        ax2.tick_params(axis='y', which='major', labelsize=48, colors='g')
        ax2.set_ylabel('SO$_2$', fontsize=48, color='g')
        plt.tight_layout()
        ax2.get_legend().remove()
        ax.get_legend().remove()
        plt.savefig('../plots/' + str(StationName) + '/' +
                    str(T1.strftime('%b_%Y')) + '.png')
    return


# To create plots:
years = [2016, 2017, 2018]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for m in months:
    plotTSNO2(SName[2], month=months[m - 1], year=years[0])

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
