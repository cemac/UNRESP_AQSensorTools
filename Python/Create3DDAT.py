def writeRec1():
    DATASET='3D.DAT' #Dataset name
    DATAVER='2.1' #Dataset version
    DATAMOD='Created using Create3DDAT.py' #Dataset message field
    fout.write('{:16}{:16}{}\n'.format(DATASET,DATAVER,DATAMOD))

def writeRec2():
    NCOMM=1 #Number of comment records to follow
    fout.write('{:1d}\n'.format(NCOMM))
    COMMENT="Currently set up to process GRIB data file from NAM's Central American/Caribbean domain" #Comments
    fout.write('{}\n'.format(COMMENT))

def writeRec3():
    IOUTW=1 #Vertical velocity flag
    IOUTQ=1 #Relative humidity flag
    IOUTC=0 #cloud/rain mixing ration flag
    IOUTI=0 #ice/snow MR flag
    IOUTG=0 #graupel MP flag
    IOSRF=0 #create surface 2D files flag
    fout.write(('{:3d}'*6+'\n').format(IOUTW,IOUTQ,IOUTC,IOUTI,IOUTG,IOSRF))

def writeRec4():
    MAPTXT='LLC' #Map projection (LLC=lat/lon)
    RLATC=(lats[iLatMinGRIB]+lats[iLatMaxGRIB])/2. #centre latitude of GRIB subset grid
    RLONC=(lons[iLonMinGRIB]+lons[iLonMaxGRIB])/2. #centre longitude of GRIB subset grid
    TRUELAT1=lats[iLatMinGRIB] #First latitude in GRIB subset grid
    TRUELAT2=lats[iLatMinGRIB+1] #Second latitude in GRIB subset grid
    X1DMN=0.0 #Not used so set to zero
    Y1DMN=0.0 #Not used so set to zero
    DXY=0.0 #Not used so set to zero
    fout.write(('{:4}{:9.4f}{:10.4f}'+'{:7.2f}'*2+'{:10.3f}'*2+'{:8.3f}'+'{:4d}'*2+'{:3d}\n').
               format(MAPTXT,RLATC,RLONC,TRUELAT1,TRUELAT2,X1DMN,Y1DMN,DXY,NX,NY,NZ))

def writeRec5():
    #Flags that aren't used unless using MM5 model
    fout.write(('{:3d}'*23+'\n').format(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))

def writeRec6():
    IBYRM=int(startDate[0:4])
    IBMOM=int(startDate[4:6])
    IBDYM=int(startDate[6:8])
    IBHRM=0
    NHRSMM5=16
    fout.write(('{:4d}'+'{:02d}'*3+'{:5d}'+'{:4d}'*3+'\n').format(IBYRM,IBMOM,IBDYM,IBHRM,NHRSMM5,NX,NY,NZ))
    
def writeRec7():
    NX1=1
    NY1=1
    NX2=NX
    NY2=NY
    NZ1=1
    NZ2=NZ
    RXMIN=lons[iLonMinGRIB]
    RXMAX=lons[iLonMaxGRIB]
    RYMIN=lats[iLatMinGRIB]
    RYMAX=lats[iLatMaxGRIB]
    fout.write(('{:4d}'*6+'{:10.4f}'*2+'{:9.4f}'*2+'\n').format(NX1,NY1,NX2,NY2,NZ1,NZ2,RXMIN,RXMAX,RYMIN,RYMAX))
    SIGMA=np.flipud(np.array(levsIncl))/1013.25
    for s in SIGMA:
        fout.write('{:6.3f}\n'.format(s))

def writeRec8():
    IELEVDOT=0 #terrain elevation above MSL (m). Set to zero for now to replicate Sara's file
    ILAND=-9 #Lansuse categories (set to -9 to replicae Sara's file)
    XLATCRS=-999
    XLONGCRS=-999
    IELEVCRS=-999
    for j in range(NY):
        JINDEX=j+1
        XLATDOT=lats[iLatMinGRIB+j]
        for i in range(NX): 
            IINDEX=i+1
            XLONGDOT=lons[iLonMinGRIB+i]
            fout.write(('{:4d}'*2+'{:9.4f}{:10.4f}{:5d}{:3d} {:9.4f}{:10.4f}{:5d}\n').format(IINDEX,JINDEX,XLATDOT,XLONGDOT,IELEVDOT,ILAND,XLATCRS,XLONGCRS,IELEVCRS))

import sys
import os
#Ensure most recent eccodes python packages are used
sys.path.insert(1,os.getenv("HOME")+'/SW/eccodes-2.6.0/lib/python2.7/site-packages')
import gribapi
import numpy as np


#####PARAMETERS
startDate='20180306'
latMinCP=11.7 #Min lat of CALPUFF grid
latMaxCP=12.2 #Max lat of CALPUFF grid
lonMinCP=273.2 #Min lon of CALPUFF grid
lonMaxCP=274.1 #Max lon of CALPUFF grid
inDir=os.getenv("HOME")+'/UNRESP_ndrive/Data/NAM_20180306'
outFile=os.getenv("HOME")+'/Data/UNRESP/3D.DAT'
levsIncl=[2,5,7,10,20,30,50,75,100,150,200,250,300,400,500,600,700,800,850,900,925,950,1000]
#####

#####SET FILENAMES
filePrefix='nam.t00z.afwaca'
fileSuffix='.tm00.grib2'
filenames=[]
filePaths=[]
for i in range(17):
    filenames.append(filePrefix+'{:02d}'.format(i*3)+fileSuffix)
    filePaths.append(os.path.join(inDir,filenames[i]))
#####

#####OPEN FIRST GRIB FILE, GET MESSAGE HANDLERS AND CLOSE
f=open(filePaths[0],'r')
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

#####DETERMINE SUBDOMAIN INDICES
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

#####SET SUBDOMAIN SIZE
NX=iLonMaxGRIB-iLonMinGRIB+1 #NX, i.e. number of longitudes in GRIB subset grid
NY=iLatMaxGRIB-iLatMinGRIB+1 #NY, i.e. number of latitudes in GRIB subset grid
NZ=len(levsIncl) #NZ, i.e. number of levels to be extracted from GRIB subset grid
#####

#####RELEASE ALL MESSAGES
for i in range(mcount):
    gribapi.grib_release(i+1)
#####

#####OPEN OUTPUT FILE
fout=open(outFile,'w')
#####

#####WRITE RECORDS
writeRec1()
writeRec2()
writeRec3()
writeRec4()
writeRec5()
writeRec6()
writeRec7()
writeRec8()

#####CLOSE OUTPUT FILE
fout.close()
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

