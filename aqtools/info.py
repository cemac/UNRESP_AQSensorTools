#!/usr/bin/env python
"""AQ information

This module was developed by CEMAC as part of the UNRESP Project.
Run this script to print useful information


Example:
    To use::


Attributes:

.. CEMAC_UNRESP_AQ:
   https://github.com/cemac/UNRESP_AQSensorTools
"""


import pandas as pd
from pandas.io.json import json_normalize
import json
import requests
import pytz
import datetime as dt
import os

pyDir = os.path.dirname(os.path.realpath(__file__))

# READ IN ACCOUNT INFO
codesFile = os.path.join(pyDir, 'AQMeshCodes.txt')
assert os.path.exists(codesFile), "Can't find file AQMeshCodes.txt"
f = open(codesFile, 'r')
lines = f.readlines()
f.close()
codecheck = ("AQMeshCodes.txt should contain exactly 3 lines:\n" +
             " A comment line,\n Account ID,\n Licence Key")
assert len(lines) == 3, codecheck
accountID = lines[1].strip()
licenceKey = lines[2].strip()
print('Genertating information.csv')
print("Further API documentation here: " +
      "https://api.airmonitors.net/3.5/documentation?key=D73341AM")

try:
    url = ("https://api.airmonitors.net/3.5/GET/" + accountID + "/" +
           licenceKey + "/stations")
    rawText = requests.get(url=url)
    rawJson = json.loads(rawText.text)
except:
    print("Couldn't access data. Are you online?" +
          " Are the codes in AQMeshCodes.txt correct?")

rawDF = json_normalize(rawJson)
rawDF.to_csv('information.csv')
