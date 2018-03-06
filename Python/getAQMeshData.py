#!/usr/bin/env python
"""
Script name: getAQMeshData.py
Author: JO'N
Date: March 2018
Purpose: Download data from one AQMesh pod using their API tool
Usage: ./getAQMeshData.py <startDate> <endDate> <variables> <outFreq>
        <startDate> - Start date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS. Or type 'start' to get data from the earliest possible time.
        <endDate> - End date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS. Or type 'end' to get data from the latest possible time.
        <variables> - List of variables to download, in single quotes separated by spaces, e.g. 'NO PM10 SO2'. Or specify 'ALL' to download all variables
        <outFreq> - "Frequency of output files. Type 'all' for all data in one file, 'daily' for one calendar day per file, or 'monthly' for one calendar month per file
Output: One or multiple csv data files (depending on chosen output frequency) with naming convention: AQMeshData_[dateRange]_[variables].csv
"""
import pandas as pd
from pandas.io.json import json_normalize
import json
import requests
from dateutil.parser import parse
import pytz
import argparse
import datetime as dt
import os

#####READ IN COMMAND LINE ARGUMENTS AND GET PYTHON DIRECTORY
parser = argparse.ArgumentParser()
parser.add_argument("startDate",help="Start date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS, e.g. 2017-01-01T00:00:00. Or type 'start' to get data from the earliest possible time.",type=str)
parser.add_argument("endDate",help="End date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS, e.g. 2017-31-01T23:59:59. Or type 'end' to get data from the latest possible time.",type=str)
parser.add_argument("variables",help="List of variables to download, in single quotes separated by spaces, e.g. 'NO PM10 SO2'. Or specify 'ALL'\
to download all variables. Full list of available variables: AIRPRES, HUM, NO, NO2, O3, PARTICULE_COUNT, PM1, PM10, PM2.5, PMTOTAL, SO2,\
  TEMP, VOLTAGE",type=str)
parser.add_argument("outFreq",help="Frequency of output files. Type 'all' to generate one output file containing all data,\
 'daily' to generate one output file per calendar day, or 'monthly' to generate one output file per calendar month",type=str)
args = parser.parse_args()
startDate=args.startDate
endDate=args.endDate
variables=args.variables
outFreq=args.outFreq
pyDir = os.path.dirname(os.path.realpath(__file__))
#####

#####PARAMETERS
allFreqs=['all','daily','monthly']
allVars=['AIRPRES', 'HUM', 'NO', 'NO2', 'O3', 'PARTICULE_COUNT', 'PM1', 'PM10', 'PM2.5', 'PMTOTAL', 'SO2', 'TEMP', 'VOLTAGE']
colOrder=['TBTimestamp','TETimestamp','SensorLabel','SensorName','PreScaled','Slope','Offset','Scaled','UnitName','Status']
#####

#####READ IN ACCOUNT INFO
codesFile = os.path.join(pyDir,'AQMeshCodes.txt')
assert os.path.exists(codesFile), "Can't find file AQMeshCodes.txt in same directory as python script"
f=open(codesFile)
hdr=f.readline()
accountID=f.readline().strip()
licenceKey=f.readline().strip()
stationID=f.readline().strip()
f.close()
#####

#####CHECK VARIABLES
if variables=='ALL':
    vars = allVars
    varStr='AllVars'
else:
    vars = [s for s in variables.split()]
    for v in vars:
        assert v in allVars, "Variable name '"+v+"' not valid. Full list of available variables: "+str(allVars)
    varStr='-'.join(vars)
#####

#####CHECK OUTPUT FREQUENCY
assert outFreq in allFreqs, "Output frequency '"+outFreq+"' not valid. List of available options: "+str(allFreqs)
#####

#####GET VALID TIME RANGE AND CHECK START/END DATES
try:
    url = "https://api.airmonitors.net/3.5/GET/"+accountID+"/"+licenceKey+"/stationdata/Period/"+stationID
    rawText = requests.get(url=url)
    rawJson = json.loads(rawText.text)
except:
    print("Couldn't access data. Are you online? Are the codes in AQMeshCodes.txt correct?")
    raise
validStart=parse(rawJson[0]['FirstTETimestamp'])
validEnd=parse(rawJson[0]['LastTBTimestamp'])
if startDate=='start':
    start=validStart
else:
    try:
        start=pytz.utc.localize(parse(startDate))
    except:
        print("Could not interpret start date - check the format")
        raise
if endDate=='end':
    end=validEnd
else:
    try:
        end=pytz.utc.localize(parse(endDate))
    except:
        print("Could not interpret end date - check the format")
        raise
assert (start-validStart).seconds >= 0, "The start date/time must come after "+str(validStart)
assert (validEnd-end).seconds >= 0, "The end date/time must come before "+str(validEnd)
assert (end-start).seconds >= 0, "The start date/time must come before the end date/time"
#####

#####SPLIT TIME RANGE INTO DAYS FOR DOWNLOAD
startDay = dt.datetime(start.year,start.month,start.day,tzinfo=pytz.UTC)
nextDay = startDay + dt.timedelta(days=1)
dateDays = [start]
while nextDay < end:
    dateDays.append(nextDay)
    nextDay+=dt.timedelta(days=1)
dateDays.append(end)
startDays=dateDays[0:-1]
endDays=dateDays[1:]
if(len(endDays)>1):
    for d,day in enumerate(endDays[:-1]):
        endDays[d]-=dt.timedelta(seconds=1)
startDaysStr=[t.strftime('%Y-%m-%dT%H:%M:%S') for t in startDays]
endDaysStr=[t.strftime('%Y-%m-%dT%H:%M:%S') for t in endDays]

#####LOAD IN DATA AND WRITE TO CSV
allData=pd.DataFrame(columns=colOrder)
for i in range(len(startDays)):
    print('Downloading data from '+startDays[i].strftime('%Y-%m-%d'))
    url = "https://api.airmonitors.net/3.5/GET/"+accountID+"/"+licenceKey+"/stationdata/"+startDaysStr[i]+"/"+endDaysStr[i]+"/"+stationID
    if variables != 'ALL':
        url=url+"/"+varStr
    rawText = requests.get(url=url)
    if rawText.text=='NO DATA WAS FOUND FOR YOUR GIVEN PARAMETERS':
        continue
    rawJson = json.loads(rawText.text)
    rawDF = json_normalize(rawJson,record_path=['Channels'],meta=['TBTimestamp', 'TETimestamp'])
    procDF=rawDF.drop(['Channel'], axis=1) #Drop channel column
    procDF=procDF[colOrder] #Reorder columns
    procDF=procDF.reindex(index=procDF.index[::-1]) #flip row so oldest date first
    if outFreq=='daily':
        fname='AQMeshData_'+startDays[i].strftime('%Y-%m-%d')+'_'+varStr+'.csv'
        print('Writing data to file '+fname)
        procDF.to_csv(os.path.join(pyDir,fname),index=False)
    else:
        allData=allData.append(procDF)
    if outFreq=='monthly' and (startDays[i].month != (startDays[i]+dt.timedelta(days=1)).month or i==len(startDays)-1):
        fname='AQMeshData_'+startDays[i].strftime('%Y-%m')+'_'+varStr+'.csv'
        print('Writing data to file '+fname)
        allData.to_csv(os.path.join(pyDir,fname),index=False)
        allData=pd.DataFrame(columns=colOrder)
if outFreq=='all':
    fname='AQMeshData_'+start.strftime('%Y-%m-%dT%H-%M-%S')+'_to_'+end.strftime('%Y-%m-%dT%H-%M-%S')+'_'+varStr+'.csv'
    print('Writing data to file '+fname)
    allData.to_csv(os.path.join(pyDir,fname),index=False)
#####
