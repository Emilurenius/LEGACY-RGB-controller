#!/bin/bash
#This script runs all necessary files for the RGB server

echo "Initializing"
sudo python3 ./RGBserver/lightController.py &
