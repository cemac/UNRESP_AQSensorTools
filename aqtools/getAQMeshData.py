#!/usr/bin/env python
"""
Script name: getAQMeshData.py
Author: JO'N/ CEMAC (University of Leeds)
Date: March 2018
Purpose: Download data from an AQMesh pod using the API tool
Usage: ./getAQMeshData.py <stationID> <startDate> <endDate> <variables> <outFreq>
        <stationID> - Unique ID of the AQMesh station from which you want to download data
        <startDate> - Start date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS. Or type 'start' to get data from the earliest possible time.
        <endDate> - End date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS. Or type 'end' to get data from the latest possible time.
        <variables> - List of variables to download, in single quotes separated by spaces, e.g. 'NO PM10 SO2'. Or specify 'ALL' to download all variables
        <outFreq> - "Frequency of output files. Type 'all' for all data in one file, 'daily' for one calendar day per file, or 'monthly' for one calendar month per file
Output: One or multiple csv data files (depending on chosen output frequency) with naming convention: AQMeshData_[stationID]_[dateRange]_[variables].csv
"""

import pandas as pd
from pandas.io.json import json_normalize
import json
import requests
from dateutil.parser import parse
import pytz
import datetime as dt
import os


def main(stationID, startDate, endDate, variables, outFreq):

    pyDir = os.path.dirname(os.path.realpath(__file__))

    # PARAMETERS
    allFreqs = ['all', 'daily', 'monthly']
    allVars = ['AIRPRES', 'HUM', 'NO', 'NO2', 'O3', 'PARTICULE_COUNT', 'PM1',
               'PM10', 'PM2.5', 'PMTOTAL', 'SO2', 'TEMP', 'VOLTAGE']
    colOrder = ['TBTimestamp', 'TETimestamp', 'SensorLabel', 'SensorName',
                'PreScaled', 'Slope', 'Offset', 'Scaled', 'UnitName', 'Status']
    # READ IN ACCOUNT INFO
    codesFile = os.path.join(pyDir, 'AQMeshCodes.txt')
    assert os.path.exists(codesFile), "Can't find file AQMeshCodes.txt in same directory as python script"
    f = open(codesFile, 'r')
    lines = f.readlines()
    f.close()
    assert len(lines) == 3, "AQMeshCodes.txt should contain exactly 3 lines: A comment line, Account ID, Licence Key"
    accountID = lines[1].strip()
    licenceKey = lines[2].strip()
    # CHECK VARIABLES
    if variables == 'ALL':
        vars = allVars
        varStr = 'AllVars'
    else:
        vars = [s for s in variables.split()]
        for v in vars:
            assert v in allVars, "Variable name '"+v+"' not valid. Full list of available variables: "+str(allVars)
        varStr='-'.join(vars)
    # CHECK OUTPUT FREQUENCY
    assert outFreq in allFreqs, "Output frequency '"+outFreq+"' not valid. List of available options: "+str(allFreqs)
    # GET VALID TIME RANGE AND CHECK START/END DATES
    # API documentation here: https://api.airmonitors.net/3.5/documentation?key=D73341AM
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
    #####

    #####LOAD IN DATA AND WRITE TO CSV
    allData=pd.DataFrame(columns=colOrder)
    print('Script started on '+dt.datetime.now().strftime('%c'))
    for i in range(len(startDays)):
        foundData=False
        print('Attempting to download data from '+startDays[i].strftime('%Y-%m-%d'))
        url = "https://api.airmonitors.net/3.5/GET/"+accountID+"/"+licenceKey+"/stationdata/"+startDaysStr[i]+"/"+endDaysStr[i]+"/"+stationID
        if variables != 'ALL':
            url=url+"/"+varStr
        rawText = requests.get(url=url)
        if not rawText.text=='NO DATA WAS FOUND FOR YOUR GIVEN PARAMETERS':
            foundData=True
            rawJson = json.loads(rawText.text)
            rawDF = json_normalize(rawJson,record_path=['Channels'],meta=['TBTimestamp', 'TETimestamp'])
            procDF=rawDF.drop(['Channel'], axis=1) #Drop channel column
            procDF=procDF[colOrder] #Reorder columns
            procDF=procDF.reindex(index=procDF.index[::-1]) #flip row so oldest date first
        if outFreq=='daily':
            if foundData:
                fname='AQMeshData_'+stationID+'_'+startDays[i].strftime('%Y-%m-%d')+'_'+varStr+'.csv'
                print('Writing data to file '+fname)
                procDF.to_csv(os.path.join(pyDir,fname),index=False)
        elif foundData:
            allData=allData.append(procDF)
        if not foundData:
            print('No data found for this day')
        if outFreq=='monthly' and (startDays[i].month != (startDays[i]+dt.timedelta(days=1)).month or i==len(startDays)-1):
            if allData.shape[0]==0:
                print('No data found for this day')
            else:
                fname='AQMeshData_'+stationID+'_'+startDays[i].strftime('%Y-%m')+'_'+varStr+'.csv'
                print('Writing data to file '+fname)
                allData.to_csv(os.path.join(pyDir,fname),index=False)
                allData=pd.DataFrame(columns=colOrder)
    if outFreq=='all':
        if allData.shape[0]==0:
            print('No data found in entire specified period')
        else:
            fname='AQMeshData_'+stationID+'_'+start.strftime('%Y-%m-%dT%H-%M-%S')+'_to_'+end.strftime('%Y-%m-%dT%H-%M-%S')+'_'+varStr+'.csv'
            print('Writing data to file '+fname)
            allData.to_csv(os.path.join(pyDir,fname),index=False)
    print('Script ended on '+dt.datetime.now().strftime('%c'))


if __name__ == '__main__':
    # READ IN COMMAND LINE ARGUMENTS
    import argparse
    parser = argparse.ArgumentParser(description="Script to download data from an AQMesh pod using the API tool",\
       epilog="Example of use: ./getAQMeshData.py 1733150 2018-01-01T00:00:00 2018-01-31T23:59:59 'SO2 NO2' daily")
    parser.add_argument("stationID", help="Unique ID of the AQMesh station from which you want to download data, e.g. 1733150 for El Panama", type=str)
    parser.add_argument("startDate", help="Start date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS, e.g. 2018-01-01T00:00:00. Or type 'start' to get data from the earliest possible time.",type=str)
    parser.add_argument("endDate", help="End date/time (UTC) of data to download, in format YYYY-MM-DDTHH:MM:SS, e.g. 2018-01-31T23:59:59. Or type 'end' to get data up to the latest possible time.",type=str)
    parser.add_argument("variables", help="List of variables to download, in single quotes separated by spaces, e.g. 'NO PM10 SO2'. Or specify 'ALL'\
    to download all variables. Full list of available variables: AIRPRES, HUM, NO, NO2, O3, PARTICULE_COUNT, PM1, PM10, PM2.5, PMTOTAL, SO2,\
      TEMP, VOLTAGE",type=str)
    parser.add_argument("outFreq",help="Frequency of output files. Type 'all' to generate one output file containing all data,\
     'daily' to generate one output file per calendar day, or 'monthly' to generate one output file per calendar month",type=str)
    args = parser.parse_args()
    # CALL MAIN ROUTINE
    main(args.stationID,args.startDate,args.endDate,args.variables,args.outFreq)
