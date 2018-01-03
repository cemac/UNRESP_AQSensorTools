#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: earjjo
"""
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib as mpl
import utm
import os
import argparse

###Read in command line arguments:
parser = argparse.ArgumentParser()
parser.add_argument("demFile", help="absolute/relative path to DEM data file",type=str)
args = parser.parse_args()
assert os.path.exists(args.demFile), "DEM data file not found. Check path."
demFile=args.demFile
#demFile='/nfs/see-fs-01_users/earjjo/Data/unresp.txt'

#read in DEM data:
f=open(demFile,'r')
lines=f.read().splitlines()
f.close()
###Pasted metadata:
#Projection    UTM
#Zone          16
#Datum         WGS84
#Spheroid      WGS84
#Units         METERS
#Zunits        NO
###
#ncols         3216
#nrows         1501
#xllcorner     431678.42183145
#yllcorner     1255168.6971331
#cellsize      91.301966063666
#NODATA_value  -9999
###
#read-in metadata:
ncols = int(lines[0].split()[1])
nrows = int(lines[1].split()[1])
xllcorner = float(lines[2].split()[1])
yllcorner = float(lines[3].split()[1])
cellsize = float(lines[4].split()[1])
NODATA_value = int(lines[5].split()[1])
#data values:
dem = np.zeros(shape=(nrows,ncols))
for i,l in enumerate(lines[6:]):
    temp=[int(x) for x in l.split()]
    dem[i,:] = temp
#set all missing values to 0:
dem0 = np.array(dem)
dem0[dem0 == NODATA_value] = 0

#x,y data:
x = np.linspace(start=xllcorner,stop=xllcorner+(ncols-1)*cellsize,num=ncols)
y = np.linspace(start=yllcorner+(nrows-1)*cellsize,stop=yllcorner,num=nrows)
xgrd,ygrd = np.meshgrid(x,y)
#lat,lon data:
lat = np.zeros(shape=(nrows,ncols))
lon = np.zeros(shape=(nrows,ncols))
for i,xv in enumerate(x):
    for j,yv in enumerate(y):
        lat[j,i] = utm.to_latlon(xv,yv,16,'P')[0]
        lon[j,i] = utm.to_latlon(xv,yv,16,'P')[1]
#np.save('/nfs/see-fs-01_users/earjjo/Data/lats',lat)
#np.save('/nfs/see-fs-01_users/earjjo/Data/lons',lon)
#lat = np.load('/nfs/see-fs-01_users/earjjo/Data/lats.npy')
#lon = np.load('/nfs/see-fs-01_users/earjjo/Data/lons.npy')

#color bar:
mycmap=cm.terrain
mycmap.set_under('white')
mynorm = mpl.colors.Normalize(0.001,np.max(dem0))

#Plot raster:
#fig=plt.figure()
#plt.pcolormesh(lon,lat,dem0,cmap=mycmap,norm=mynorm)
#plt.show()

#Plot surface on top of basemap:
mymap = Basemap(llcrnrlon=np.amin(lon),llcrnrlat=np.amin(lat),
            urcrnrlon=np.amax(lon),urcrnrlat=np.amax(lat),
            resolution='h',projection='tmerc',lat_0=0,lon_0=-90)
xm,ym  = mymap(-86.251389,12.136389) #managua
x2,y2 = mymap(lon,lat) #new x2,y2 aren't in UTM but some coords relative to the map
stride=100
zscl=10
opacity=0.75
#
fig=plt.figure()
ax = Axes3D(fig)
ax.plot_surface(x2,y2,dem0,rstride=stride,cstride=stride,
                cmap=mycmap,norm=mynorm,alpha=opacity,linewidth=0)
ax.add_collection3d(mymap.drawcoastlines(zorder=20))
ax.add_collection3d(mymap.drawcountries(zorder=20))
ax.scatter(xm,ym,color="red",zorder=20)
ax.text(xm,ym,0.01,"Managua",zorder=20)
ax.set_zlim(0,np.amax(dem0)*zscl)
plt.show()