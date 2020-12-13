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
            startTime = time.time()
            x = 0
            while startTime + 2 != time.time():
                print(x)
                x +=1
                if GPIO.input(clapSensor):
                    print("Double clap!")
                    time.sleep(0.2)
                    break
finally:
    GPIO.cleanup()