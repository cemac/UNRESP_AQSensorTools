#!/usr/bin/bash

###Script to transfer latest El Panama AQ-Mesh data files to the shared N-Drive workspace
###(Crobtab only runs when earjjo is personally logged in)

#Make sure we're in the right directory
cd /nfs/see-fs-01_users/earjjo/gitRepos/UNRESP/Python

#delete current 'latest data' file on N-Drive
rm -f /nfs/see-fs-01_users/earjjo/UNRESP_ndrive/AQMeshData/1733150_ElPanama/AQMeshData_1733150*_to_*.csv

#sync latest files with N-Drive
echo $(date) >> updateNDrive.log
rsync -avzh 1733150_ElPanama /nfs/see-fs-01_users/earjjo/UNRESP_ndrive/AQMeshData/ >> updateNDrive.log
