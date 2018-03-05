def writeRec1(fout):
    fout.write('{:16}{:16}{}'.format('3D.DAT','2.1','Created using Create3DDAT.py'))
    


#import sys
import os
#Ensure most recent eccodes python packages are used
#sys.path.insert(1,os.getenv("HOME")+'/SW/eccodes-2.6.0/lib/python2.7/site-packages')
#import gribapi
#import numpy as np


#####PARAMETERS
latMin=11.7 #Min lat of CALPUFF grid
latMax=12.2 #Max lat of CALPUFF grid
lonMin=273.2 #Min lon of CALPUFF grid
lonMax=274.1 #Max lon of CALPUFF grid
outFile=os.getenv("HOME")+'/Data/UNRESP/3D.DAT'
#####

#####OPEN GRIB FILE, GET MESSAGE HANDLERS AND CLOSE
#INPUT=os.getenv("HOME")+'/Data/UNRESP/nam.t00z.afwaca00.tm00.grib2'
#f=open(INPUT,'r')
#gribapi.grib_multi_support_on()
#mcount = gribapi.grib_count_in_file(f) #number of messages in file
#gids = [gribapi.grib_new_from_file(f) for i in range(mcount)]
#f.close()
######

#####OPEN OUTPUT FILE
fout=open(outFile,'w')
#####

#####WRITE RECORDS
writeRec1(fout)

#####CLOSE OUTPUT FILE
fout.close()
#####

######RELEASE ALL MESSAGES
#for i in range(mcount):
#    gribapi.grib_release(i+1)
######

##Create list of message variable names
#varNames=[]
#for i in range(mcount):
#    gid = gids[i]
#    varNames.append(gribapi.grib_get(gid,'shortName'))
#
##Get gids of important messages
#gidMSLP=varNames.index("prmsl")+1
#gidU10=varNames.index("10u")+1
#gidV10=varNames.index("10v")+1
#gidU=[i+1 for i in range(len(varNames)) if varNames[i] == 'u']
#gidV=[i+1 for i in range(len(varNames)) if varNames[i] == 'u']
#
##Get lats and lons of GRIB data
#lats=gribapi.grib_get_array(gidMSLP,'distinctLatitudes')
#lons=gribapi.grib_get_array(gidMSLP,'distinctLongitudes')
#
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

