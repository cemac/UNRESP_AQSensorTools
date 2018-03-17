#!/usr/bin/env python
"""
Script name: getLatestAQMeshData.py
Author: JO'N
Date: March 2018
Purpose: Download AQ-Mesh data from El Panama pod for present day and condense all daily files into one file at end of calendar month
"""

import datetime as dt
import getAQMeshData

now=dt.datetime.now()
startOfToday=dt.datetime(now.year,now.month,now.day)
startOfTodayStr=startOfToday.strftime('%Y-%m-%dT%H:%M:%S')

getAQMeshData.main('1733150',startOfTodayStr,'end','ALL','all')
