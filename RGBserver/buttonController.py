import time
import RPi.GPIO as GPIO
import requests


# Pins definitions
btn_pin = 17
led_pin = 12

# Set up pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(btn_pin, GPIO.IN)
GPIO.setup(led_pin, GPIO.OUT)

# If button is pushed, light up LED
try:
    lastBtnState = False
    btnState = False
    while True:
        if GPIO.input(btn_pin):
            nochange = False
            x = 0
            while x < 100000:
                if not GPIO.input(btn_pin):
                    nochange = True
                    break
                else:
                    x += 1
            if nochange == False:
                btnState = True
                time.sleep(0.0001)
            else:
                nochange = False
                time.sleep(0.0001)
        else:
            btnState = False
        
        if btnState != lastBtnState:
            print("button pushed!")
            lastBtnState = btnState
            response = requests.get("http://localhost:3000/lightstate?toggle=change")
            print(response)

# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()
