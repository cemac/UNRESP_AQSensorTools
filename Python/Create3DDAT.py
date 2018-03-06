def writeRec1():
    fout.write('{:16}{:16}{}\n'.format('3D.DAT','2.1','Created using Create3DDAT.py'))

def writeRec2():
    fout.write('1\n')
    fout.write("Currently set up to process GRIB data file from NAM's Central American/Caribbean domain\n")

def writeRec3():
    fout.write(('{:3d}'*6+'\n').format(1,1,0,0,0,0))

def writeRec4():
    cenLat=(lats[iLatMinGRIB]+lats[iLatMaxGRIB])/2.
    cenLon=(lons[iLonMinGRIB]+lons[iLonMaxGRIB])/2.
    firstTrueLat=lats[iLatMinGRIB]
    secondTrueLat=lats[iLatMinGRIB+1]
    NX=iLonMaxGRIB-iLonMinGRIB+1
    NY=iLatMaxGRIB-iLatMinGRIB+1
    NZ=len(levsIncl)
    fout.write(('{:4}{:9.4f}{:10.4f}{:7.2f}{:7.2f}{:10.3f}{:10.3f}{:8.3f}{:4d}{:4d}{:3d}\n').
               format('LLC',cenLat,cenLon,firstTrueLat,secondTrueLat,0.0,0.0,0.0,NX,NY,NZ))


import sys
import os
#Ensure most recent eccodes python packages are used
sys.path.insert(1,os.getenv("HOME")+'/SW/eccodes-2.6.0/lib/python2.7/site-packages')
import gribapi
import numpy as np


#####PARAMETERS
latMinCP=11.7 #Min lat of CALPUFF grid
latMaxCP=12.2 #Max lat of CALPUFF grid
lonMinCP=273.2 #Min lon of CALPUFF grid
lonMaxCP=274.1 #Max lon of CALPUFF grid
outFile=os.getenv("HOME")+'/Data/UNRESP/3D.DAT'
levsIncl=[2,5,7,10,20,30,50,75,100,150,200,250,300,400,500,600,700,800,850,900,925,950,1000]
#####

#####OPEN GRIB FILE, GET MESSAGE HANDLERS AND CLOSE
INPUT=os.getenv("HOME")+'/Data/UNRESP/nam.t00z.afwaca00.tm00.grib2'
f=open(INPUT,'r')
gribapi.grib_multi_support_on()
mcount = gribapi.grib_count_in_file(f) #number of messages in file
gids = [gribapi.grib_new_from_file(f) for i in range(mcount)]
f.close()
#####

#####CREATE LIST OF MESSAGE VARIABLE NAMES
varNames=[]
levels=[]
for i in range(mcount):
    gid = gids[i]
    varNames.append(gribapi.grib_get(gid,'shortName'))
    levels.append(gribapi.grib_get(gid,'level'))
#####

#####GET REQUIRED GIDS
gidMSLP=varNames.index("prmsl")+1
#gidU10=varNames.index("10u")+1
#gidV10=varNames.index("10v")+1
gidU=[i+1 for i in range(len(varNames)) if (varNames[i] == 'u' and levels[i] in levsIncl)]
#gidV=[i+1 for i in range(len(varNames)) if varNames[i] == 'u']
#####

#####GET LATS AND LONS
lats=gribapi.grib_get_array(gidMSLP,'distinctLatitudes')
lons=gribapi.grib_get_array(gidMSLP,'distinctLongitudes')
#####

#####DETERMINE SUBSET INDICES
for i in range(len(lats)-1):
    if lats[i+1] >= latMinCP:
        iLatMinGRIB=i
        break
for i in range(len(lats)-1):
    if lats[i+1] > latMaxCP:
        iLatMaxGRIB=i+1
        break
for i in range(len(lons)-1):
    if lons[i+1] >= lonMinCP:
        iLonMinGRIB=i
        break
for i in range(len(lons)-1):
    if lons[i+1] > lonMaxCP:
        iLonMaxGRIB=i+1
        break
#####  

#####OPEN OUTPUT FILE
fout=open(outFile,'w')
#####

#####WRITE RECORDS
writeRec1()
writeRec2()
writeRec3()
writeRec4()

#####CLOSE OUTPUT FILE
fout.close()
#####

#####RELEASE ALL MESSAGES
for i in range(mcount):
    gribapi.grib_release(i+1)
#####



##Get MSLP field
#iterid=gribapi.grib_iterator_new(gidMSLP,0)
#missingValue=gribapi.grib_get_double(gidMSLP,"missingValue")
#while 1:
#    result=gribapi.grib_iterator_next(iterid)
#    if not result: break
#    [lat,lon,value] = result 
#    if latMin < lat < latMax and lonMin < lon < lonMax:
#        if value == missingValue:
#            print("missing")
#        else:
#            print("lat=%.3f, lon=%.3f, value=%.3f" % (lat,lon,value))
#gribapi.grib_iterator_delete(iterid)

