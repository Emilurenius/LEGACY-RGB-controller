#!/bin/bash
#This script runs all necessary files for the RGB server
#Currently not working

echo "Initializing"
node ./RGBserver/app.js 3000 &
python3 ./RGBserver/clapSensor.py &
python3 ./ws281xSC_module/alarmController.py &
python3 app.py &
sudo python3 ./RGBserver/lightController.py