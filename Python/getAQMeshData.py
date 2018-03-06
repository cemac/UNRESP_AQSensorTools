from pandas.io.json import json_normalize
import json
import requests
from dateutil.parser import parse
import pytz
import argparse
import datetime as dt
import os
import pandas as pd

#####READ IN COMMAND LINE ARGUMENTS AND GET PYTHON DIRECTORY
#parser = argparse.ArgumentParser()
#parser.add_argument("startDate",help="Start date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS, e.g. 2017-01-01T00:00:00",type=str)
#parser.add_argument("endDate",help="End date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS, e.g. 2017-31-01T23:59:59",type=str)
#parser.add_argument("variables",help="List of variables to download, in single quotes separated by spaces, e.g. 'NO PM10 SO2'. Or specify 'ALL'\
#to download all variables. Full list of available variables: AIRPRES, HUM, NO, NO2, O3, PARTICULE_COUNT, PM1, PM10, PM2.5, PMTOTAL, SO2,\
#  TEMP, VOLTAGE",type=str)
#parser.add_argument("outFreq",help="Frequency of output files. Type 'all' to generate one output file containing all data,\
#  or 'daily' to generate one output file per calendar day",type=str)
#args = parser.parse_args()
#startDate=args.startDate
#endDate=args.endDate
#variables=args.variables
#pyDir = os.path.dirname(os.path.realpath(__file__))
#
startDate="2018-01-01T12:00:00"
endDate="2018-01-05T01:00:00"
variables='NO PM10 SO2'
outFreq='all'
pyDir='/nfs/see-fs-01_users/earjjo/gitRepos/UNRESP/Python/'
#####

#####PARAMETERS
allFreqs=['all','daily']
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
start=pytz.utc.localize(parse(startDate))
end=pytz.utc.localize(parse(endDate))
assert (start-validStart).seconds >+ 0, "The start date/time must come after "+str(validStart)
assert (validEnd-end).seconds >= 0, "The end date/time must come before "+str(validEnd)
assert (end-start).seconds >= 0, "The start date/time must come before the end date/time"
#####

#####SPLIT TIME RANGE INTO DAYS FOR DOWNLOAD
startDay = dt.datetime(start.year,start.month,start.day,tzinfo=pytz.UTC)
dateDays = [start]
nextDay = startDay + dt.timedelta(days=1)
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
for i in range(len(startDaysStr)):
    print('downloading data from '+startDays[i].strftime('%Y-%m-%d'))
    url = "https://api.airmonitors.net/3.5/GET/"+accountID+"/"+licenceKey+"/stationdata/"+startDaysStr[i]+"/"+endDaysStr[i]+"/"+stationID
    if variables != 'ALL':
        url=url+"/"+varStr
    rawText = requests.get(url=url)
    rawJson = json.loads(rawText.text)
    rawDF = json_normalize(rawJson,record_path=['Channels'],meta=['TBTimestamp', 'TETimestamp'])
    procDF=rawDF.drop(['Channel'], axis=1)
    procDF=procDF[colOrder]
    procDF=procDF.reindex(index=procDF.index[::-1])
    if outFreq=='daily':
        fname='AQMeshData_'+startDays[i].strftime('%Y-%m-%d')+'_'+varStr+'.csv'
        procDF.to_csv(os.path.join(pyDir,fname),index=False)
    else:
        allData=allData.append(procDF)
if outFreq=='all':
    fname='AQMeshData_'+start.strftime('%Y-%m-%dT%H-%M-%S')+'_to_'+end.strftime('%Y-%m-%dT%H-%M-%S')+'_'+varStr+'.csv'
    allData.to_csv(os.path.join(pyDir,fname),index=False)
#####
