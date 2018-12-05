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
latMin = 11.7
latMax = 12.2
lonMin = -86.7
lonMax = -86.0
bmap = Basemap(llcrnrlon=lonMin, llcrnrlat=latMin, urcrnrlon=lonMax, urcrnrlat=latMax)
esri_url = \
    "http://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?\
bbox=%s,%s,%s,%s&\
bboxSR=%s&\
imageSR=%s&\
size=%s,%s&\
dpi=%s&\
format=png32&\
f=image" %\
(bmap.llcrnrlon, bmap.llcrnrlat, bmap.urcrnrlon, bmap.urcrnrlat, bmap.epsg, bmap.epsg, xpixels, bmap.aspect*xpixels, 96)
ESRIimg = mpimg.imread(esri_url)
