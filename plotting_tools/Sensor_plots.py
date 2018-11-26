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


example = pd.read_csv('../data/AQMeshData_1733150_2018-10-23_SO2-NO2.csv')
allSO2 = pd.DataFrame(columns=example.columns)
allNO2 = pd.DataFrame(columns=example.columns)
pname = '/nfs/earcemac/projects/unresp/ForecastVisualized/UNRESP_AQSensorTools/data/*'
for rw in glob.iglob(pname):
    day_data = pd.read_csv(rw)
    NO2 = day_data[day_data.SensorLabel=='NO2']
    SO2 = day_data[day_data.SensorLabel!='NO2']
    NO2_valid=NO2[NO2.Status == 'Valid']
    SO2_valid=SO2[SO2.Status == 'Valid']
    allSO2 = pd.concat([allSO2, SO2_valid]).reset_index(drop=True)
    allNO2 = pd.concat([allNO2, NO2_valid]).reset_index(drop=True)
    
allNO2['TBTimestamp'] = pd.to_datetime(allNO2['TBTimestamp'])
allSO2['TBTimestamp'] = pd.to_datetime(allSO2['TBTimestamp'])

# plot whole dataset
plt.figure(figsize=(100,8))    
ax = plt.gca()
allSO2.plot.line(x='TBTimestamp', y='Scaled', color='red', ax=ax)
allNO2.plot.line(x='TBTimestamp', y='Scaled', secondary_y=True, ax=ax)
plt.savefig('2018.png')
plt.figure(figsize=(100,8))    
ax = plt.gca()
allSO2.plot.line(x='TBTimestamp', y='Scaled', color='red', ax=ax)
plt.savefig('SO22018.png')
plt.figure(figsize=(20,8))    
ax = plt.gca()
allNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
plt.savefig('NO22018.png')

# plot first working period jan to april
plt.figure(figsize=(20,8)) 
mask = (allNO2['TBTimestamp'] > '2018-01-01 00:00:00') & (allNO2['TBTimestamp'] <= '2018-04-01 00:00:00')
J2ANO2 = allNO2.loc[mask]
ax = plt.gca()
J2ANO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
plt.savefig('J2A_NO22018.png')


# plot first working period jan to april
plt.figure(figsize=(20,8)) 
mask = (allNO2['TBTimestamp'] > '2018-04-01 00:00:00') & (allNO2['TBTimestamp'] <= '2018-06-10 00:00:00')
A2JNO2 = allNO2.loc[mask]
ax = plt.gca()
A2JNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
plt.savefig('A2J_NO22018.png')

# plot first working period Aug to Oct
plt.figure(figsize=(20,8)) 
mask = (allNO2['TBTimestamp'] > '2018-08-01 00:00:00') & (allNO2['TBTimestamp'] <= '2018-10-12 00:00:00')
A2ONO2 = allNO2.loc[mask]
ax = plt.gca()
A2ONO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
plt.savefig('A2O_NO22018.png')


# plot first working period Aug to Oct
plt.figure(figsize=(20,8)) 
mask = (allNO2['TBTimestamp'] > '2018-10-18 00:00:00') & (allNO2['TBTimestamp'] <= '2018-11-20 00:00:00')
RNO2 = allNO2.loc[mask]
ax = plt.gca()
RNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax)
plt.savefig('recent_NO22018.png')