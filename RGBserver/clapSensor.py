import time
import RPi.GPIO as GPIO
import requests

clapSensor = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(clapSensor, GPIO.IN)

try:
    if GPIO.input(clapSensor):
        print("Clap detected")
finally:
    GPIO.cleanup()