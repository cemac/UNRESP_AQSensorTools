# -*- coding: utf-8 -*-
"""Sensor Plotter

This module was developed by CEMAC as part of the UNRESP Project.
This script takes data from the AQ Sensors (obtained by getAQMeshData.py)
and plots the data.

Example:
    To use::

Attributes:

.. CEMAC_AQMesh:
   https://github.com/cemac/UNRESP_AQSensorTools
"""

import pandas as pd
import glob
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from pytz import timezone
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io import shapereader
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from matplotlib.font_manager import FontProperties
import cartopy.io.img_tiles as cimgt


# Station lat lonts
fname = '../aqtools/information.csv'
data = pd.read_csv(fname)

Stations = data.StationName

towns = (' El Panama', ' Rigoberto', ' Pacaya', ' El Crucero',
         ' La Concepcion', ' Masaya', ' San Marcos', ' Jinotepe')
townCoords = ((-86.2058, 11.972), (-86.2021, 11.9617), (-86.3013, 11.9553),
              (-86.3113, 11.9923), (-86.189772, 11.936161),
              (-86.096053, 11.973523), (-86.20317, 11.906584),
              (-86.19993, 11.85017))
volcCoords = (-86.1608, 11.9854)


font = FontProperties()
font.set_weight('bold')
font.set_family('monospace')


extent = [-86.7, -86.0, 11.7, 12.2]
request = cimgt.OSM()

fig = plt.figure(figsize=(9, 13))
ax = plt.axes(projection=request.crs)
gl = ax.gridlines(draw_labels=True, alpha=0.2)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# ax.set_extent(extent)
ax.set_extent(extent)
ax.add_image(request, 10, interpolation='spline36')
for i, town in enumerate(towns):
    ax.plot(townCoords[i][0], townCoords[i]
                         [1], 'og', markersize=4, transform=ccrs.Geodetic())
ax.plot(volcCoords[0], volcCoords[1], '^r',
        markersize=6, transform=ccrs.Geodetic())
plt.show()
