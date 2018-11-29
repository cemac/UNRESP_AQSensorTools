<div align="center">
<a href="https://www.cemac.leeds.ac.uk/">
  <img src="https://github.com/cemac/cemac_generic/blob/master/Images/cemac.png"></a>
  <br>
</div>

# UNRESP AQ Mesh #

Repository for the [UNRESP](https://vumo.cloud/) AQ Mesh. Persistent volcanic emissions around Masaya, Nicaragua

## Description ##

Fetches all SO2 and NO2 data from Jan 2018 from the El Panama AQMesh pod station and produces one output file per day. The script makes use of the Air Monitors API; documentation can be found [here](https://api.airmonitors.net/3.5/documentation?key=D73341AM).


## Requirements ##

* AQ Mesh API access
* Python (standard anaconda install) *yml coming soon*

## Usage ##

1. **Retrieve data** (aqtools)
  **NB** requires Licence key not stored in Repository
  * To find out station information such as co-ordinates run:
  `.\info.py`
  * To retrieve data from each station use `getAQMeshData.py`. Information on how to run this python script can be printed directly to the terminal by typing `getAQMeshData.py --help`, but an example would be:
  ```sh
  ./getAQMeshData.py 1733150 2018-01-01T00:00:00 2018-01-31T23:59:59 'SO2 NO2' daily
  ```
  which would fetch all SO2 and NO2 data from Jan 2018 from the El Panama AQMesh pod station and produce one output file per day.

  * Another script called `getLatestAQMeshData.py` which can be called once an hour (via a cronjob) to get the latest data from the El Panama station.
  ```sh
  30 * * * * cd /nfs/see-fs-01_users/earjjo/gitRepos/UNRESP/Python && ./updateAQMeshData.sh
  ```
  This relies on a directory called '1733150_ElPanama' existing within the same directory as the above shell and python scripts.

2. **Plotting Sensor data** (plotting_tools)
    * `Sensor_plots.py` plotting all data *in development*


## Licence information ##

This project is currently licensed under the [MIT license](https://choosealicense.com/licenses/mit/).

<hr>

## Acknowledgements ##

*Coming soon*

<hr>
