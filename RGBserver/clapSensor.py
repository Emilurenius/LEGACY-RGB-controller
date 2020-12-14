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
            time.sleep(0.7)
            startTime = datetime.datetime.now().timestamp()
            print("Started waiting for double clap:", startTime)
            while datetime.datetime.now().timestamp() - startTime < 1:
                if GPIO.input(clapSensor):
                    print("Double clap!")
                    response = requests.get("http://localhost:3000/lightstate?toggle=change")
                    print(response)
                    break
            time.sleep(0.1)
finally:
    GPIO.cleanup()