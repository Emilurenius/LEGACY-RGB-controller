#!/bin/sh

#This file starts all scripts that act like a middle man between the server and hardware.
sudo python3 lightController.py &
python3 clapSensor.py