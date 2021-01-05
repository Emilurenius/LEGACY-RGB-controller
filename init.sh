#!/bin/sh

sudo python3 lightController.py &
python3 clapSensor.py &
node RGBserver/app.js 300 