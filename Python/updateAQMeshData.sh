#!/usr/bin/bash

###Script to keep the El Panama AQ-Mesh data files up to date

#delete current 'latest data' file
rm -f 1733150_ElPanama/AQMeshData_1733150*_to_*.csv

#run python script to get new 'latest data' file
./getLatestAQMeshData.py >> updateAQMeshData.log

#move new 'latest data' file (and potentially new daily/monthly files) to the relevant subdirectory 
mv -f AQMeshData_1733150*.csv 1733150_ElPanama/.
