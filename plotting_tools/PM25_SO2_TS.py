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


def getdata(StationName, var1='PM2.5', var2=None):
    pname = '../data/' + StationName + '/AQMeshData*_2017*.csv'
    for rw in glob.iglob(pname):
        day_data = pd.read_csv(rw)
        data = day_data[day_data.SensorLabel == var1]
        data_valid = data[data.Status == 'Valid']
        alldata = data_valid.reset_index(drop=True)
        if var2 is not None:
            data2 = day_data[day_data.SensorLabel == var2]
            data2_valid = data2[data2.Status == 'Valid']
            alldata2 = data2_valid.reset_index(drop=True)
    alldata['TBTimestamp'] = pd.to_datetime(alldata['TBTimestamp'])
    alldata['TBTimestamp'].apply(lambda x: datetime.replace(x, tzinfo=None))
    alldata['date'] = alldata['TBTimestamp'].apply(lambda x: x.strftime("%Y %b"))
    if var2 is not None:
        alldata2['TBTimestamp'] = pd.to_datetime(alldata2['TBTimestamp'])
        alldata2['TBTimestamp'].apply(lambda x: datetime.replace(x, tzinfo=None))
        alldata2['date'] = alldata2['TBTimestamp'].apply(lambda x: x.strftime("%Y %b"))
    return alldata, alldata2


def plotdata(StationName, month=1, year=2016, ymax=100,
             var1='PM2.5', var1df=None, var2=None, var2df=None):
    T1 = datetime(year, month, 1, 0, 0, 0).replace(tzinfo=None)
    if month == 12:
        T2 = datetime(year, month, 31, 0, 0, 0).replace(tzinfo=None)
    else:
        T2 = datetime(year, month + 1, 1, 0, 0, 0).replace(tzinfo=None)
    plt.figure(figsize=(30, 10))
    ax = plt.gca()
    ax.set_title(StationName + ' ' + var1 + '\n', fontsize=48)
    if not var1df.empty:
        var1df.plot.line(x='TBTimestamp', y='Scaled', ax=ax, color='b')
        ax.set_xlim([T1, T2])
        ax.set_ylim([0, 500])
        ax.set_ylabel(var1, fontsize=48, color='b')
        ax.tick_params(axis='both', which='major', labelsize=48)
        ax.tick_params(axis='y', which='major', labelsize=48, colors='b')
        ax.xaxis.set_major_formatter(myFmtday)
        ax.xaxis_date()
        ax.set_xlabel(T1.strftime('%b %Y'), fontsize=48)
        ax.get_legend().remove()
        plt.tight_layout()
        plt.savefig('../plots/' + str(StationName) + '/' + var1 +
                    str(T1.strftime('%b_%Y')) + '.png')
        plt.close()
    if var2 is None:
        return
    plt.figure(figsize=(30, 10))
    ax = plt.gca()
    ax.set_title(StationName + ' ' + var2 + '\n', fontsize=48)
    if not var2df.empty:
        var2df.plot.line(x='TBTimestamp', y='Scaled', ax=ax, color='g')
        ax.set_xlim([T1, T2])
        ax.set_ylim([0, 1200])
        ax.set_ylabel(var2, fontsize=48, color='g')
        ax.tick_params(axis='both', which='major', labelsize=48)
        ax.tick_params(axis='y', which='major', labelsize=48, colors='g')
        ax.xaxis.set_major_formatter(myFmtday)
        ax.xaxis_date()
        ax.set_xlabel(T1.strftime('%b %Y'), fontsize=48)
        ax.get_legend().remove()
        plt.tight_layout()
        date = T1.strftime('%b_%Y')
        print(date)
        plt.savefig('../plots/' + str(StationName) + '/' + var2 +
                    str(date) + '.png')
        plt.close()

    if not var1df.empty:
        plt.figure(figsize=(30, 10))
        ax = plt.gca()
        ax.set_title(StationName + ' ' + var1 + ' ' + var2 + '\n', fontsize=48)
        var1df.plot.line(x='TBTimestamp', y='Scaled', ax=ax, color='b')
        ax.set_xlim([T1, T2])
        ax.set_ylim([0, 500])
        ax.set_ylabel(var1, fontsize=48, color='b')
        ax.tick_params(axis='both', which='major', labelsize=48)
        ax.tick_params(axis='y', which='major', labelsize=48, colors='b')
        ax.xaxis.set_major_formatter(myFmtday)
        ax.xaxis_date()
        ax.set_xlabel(T1.strftime('%b %Y'), fontsize=48)
        ax2 = ax.twinx()
        var2df.plot.line(x='TBTimestamp', y='Scaled', ax=ax2, color='g')
        ax2.set_xlim([T1, T2])
        ax2.set_ylim([0, 1200])
        ax2.xaxis_date()
        ax2.xaxis.set_major_formatter(myFmtday)
        ax2.tick_params(axis='y', which='major', labelsize=48, colors='g')
        ax2.set_ylabel(var2, fontsize=48, color='g')
        plt.tight_layout()
        ax2.get_legend().remove()
        ax.get_legend().remove()
        date = T1.strftime('%b_%Y')
        plt.savefig('../plots/' + str(StationName) + '/' + var1 + var2 +
                    date + '.png')
        plt.close()
    return


# To create plots:
years = [2017, 2018, 2019]
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for s in SName:
    pm25df, so2df = getdata(s, var1='PM2.5', var2='SO2')
    for m in months:
        plotdata(s, month=months[m - 1], year=years[0], var1='PM2.5',
                 var1df=pm25df, var2='SO2', var2df=so2df)
    for m in months:
        plotdata(s, month=months[m - 1], year=years[1], var1='PM2.5',
                 var1df=pm25df, var2='SO2', var2df=so2df)
    for m in months:
        plotdata(s, month=months[m - 1], year=years[2], var1='PM2.5',
                 var1df=pm25df, var2='SO2', var2df=so2df)
