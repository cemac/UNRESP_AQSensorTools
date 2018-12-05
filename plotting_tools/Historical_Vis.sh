#!/usr/bin/bash
cwd=$(pwd)
stationnames=("SanJu1" "ElCrucero" "SanJuan2" "785150" "Pacaya" "Rigoberto" "861150" "Met" "ElPanama")
VIZPATH=~/public_html/UNRESP/UNRESP_VIZ/AQSensor/
echo "Generating plots"
python All_timeseries.py
echo "Generated plots"
for i in ${!stationnames[*]};
  do
    fname=${stationnames[$i]}
    if [ ! -e $VIZPATH$fname ];
    then
      mkdir $VIZPATH$fname
    fi
    fileroot=~/UNRESP_AQtools/data/$fname
    files=${'/all*2018.png'}
    cp -p $fileroot$files $VIZPATH$fname
    cd $VIZPATH$fname
    setfacl -m other:r-x *
    chmod og+rx *
    cd $cwd
done
