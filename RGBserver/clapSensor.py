import time, datetime
import RPi.GPIO as GPIO
import requests

clapSensor = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(clapSensor, GPIO.IN)

try:
    while True:
        if GPIO.input(clapSensor):
            print("Clap detected")
            time.sleep(0.2)
            startTime = datetime.datetime.now()
            print(startTime)
            print(startTime + 5)
finally:
    GPIO.cleanup()