#!/usr/bin/env python
"""
Script name: getLatestAQMeshData.py
Author: JO'N
Date: March 2018
Purpose: Download latest AQ-Mesh data from El Panama pod and condense all daily files into one file at end of calendar month
"""

import datetime as dt
import getAQMeshData

#Set download start date to yesterday at 00:00:00:
now=dt.datetime.now()
startOfYday=dt.datetime(now.year,now.month,now.day)-dt.timedelta(days=1)
startOfYdayStr=startOfYday.strftime('%Y-%m-%dT%H:%M:%S')

#Download data up to most recent time:
getAQMeshData.main('1733150',startOfYdayStr,'end','ALL','all')

#If into new day, download full day from 2 days ago
if (now-dt.timedelta(hours=1)).day != now.day:
    startOf2DaysAgo=dt.datetime(now.year,now.month,now.day)-dt.timedelta(days=2)
    startOf2DaysAgoStr=startOf2DaysAgo.strftime('%Y-%m-%dT%H:%M:%S')
    getAQMeshData.main('1733150',startOf2DaysAgoStr,startOfYdayStr,'ALL','daily')
    
