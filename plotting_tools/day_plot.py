#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Sensor Plotter

UNDER CONSTRUCTION, works current;y but not nicely

This module was developed by CEMAC as part of the UNRESP Project.
This script takes data from the AQ Sensors (obtained by getAQMeshData.py)
and plots the data for 1 file

Example:
    To use::

Attributes:

To do:
    Tidy up date extraction
    Test on different file lengths
    Alter ylims?
    Facility binning data?

.. CEMAC_stomtracking:
   https://github.com/cemac/UNRESP_AQSensorTools
"""

import pandas as pd
import glob
from matplotlib.dates import DateFormatter
from pytz import timezone
from datetime import datetime
from Sensor_plots import *
import argparse
from dateutil.parser import parse
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# READ IN COMMAND LINE ARGUMENTS
dstring = ("Used to generate a series (48hrs) of static and interactive" +
           "(google) maps \n showing SO2 concentrations around the Masaya " +
           "volcano, as predicted by the CALPUFF dispersion model")
hstring = ("Date string, format YYYYMMDD, of the current CALPUFF run. Used " +
           "to + locate \n  directory containing the SO2 output files (with " +
           "assumed naming convention 'concrec0100**.dat', \n where '**' " +
           " goes from '01' through to '48'")
parser = argparse.ArgumentParser(description=dstring)
parser.add_argument('--file', help='data file name',
                    default='AQMeshData_*csv', type=str)
parser.add_argument('--var', help='Select variable e.g. NO2 (default)',
                    default='NO2', type=str)
parser.add_argument('--out',
                    help='Output filename, defaults to date_var_plot.pdf',
                    default='plot', type=str)
# bin the data
binLims = [0, 10, 350, 600, 2600, 9000, 14000]
bin_lables = ["vlow", "low", "moderate", "mod high", "high", "vhigh"]
args = parser.parse_args()
var = args.var
out = args.out
filen = args.file
for rw in glob.iglob(filen):
    day_data = pd.read_csv(rw)
    NO2 = day_data[day_data.SensorLabel == var]
    NO2_valid = NO2[NO2.Status == 'Valid']
    allNO2 = NO2_valid.reset_index(drop=True)
allNO2['TBTimestamp'] = pd.to_datetime(allNO2['TBTimestamp'])
allNO2['TBTimestamp'].apply(lambda x: datetime.replace(x, tzinfo=None))
allNO2['date'] = allNO2['TBTimestamp'].apply(lambda x: x.strftime("%Y %b"))
plt.figure(figsize=(30, 10))
ax = plt.gca()
# ax.set_title(var + str(T1.strftime('%b_%Y')) + '\n', fontsize=48)
ax.set_title(var + '\n', fontsize=48)
if not allNO2.empty:
    allNO2.plot.line(x='TBTimestamp', y='Scaled', ax=ax, color='b')
    ax.set_ylabel('NO$_2$', fontsize=48, color='b')
    ax.tick_params(axis='both', which='major', labelsize=48)
    ax.tick_params(axis='y', which='major', labelsize=48, colors='b')
    ax.xaxis.set_major_formatter(myFmtday)
    ax.xaxis_date()
    # ax.set_xlabel(T1.strftime('%b %Y'), fontsize=48)
    ax2 = ax.twinx()
    ax.get_legend().remove()
    # TO DO: Extract date from csv file
    plt.savefig('date_' + '_' + var + '_plot.png')
else:
    print('no ' + var + 'data in ' + filen)
