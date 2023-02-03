#!/bin/bash
#This script runs all necessary files for the RGB server
#Currently not working

echo "Initializing"
node ./RGBserver/app.js 3000 &
sudo python3 ./RGBserver/lightController.py