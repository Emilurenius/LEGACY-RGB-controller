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
            startTime = datetime.datetime.now().timestamp()
            print(startTime)
            x = 0
            while startTime < startTime + 50:
                print(x)
                x +=1
                if GPIO.input(clapSensor):
                    print("Double clap!")
                    break
            time.sleep(0.1)
finally:
    GPIO.cleanup()