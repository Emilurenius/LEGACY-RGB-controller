import time, datetime
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
            change = False
            startTime = datetime.datetime.now().timestamp()
            while datetime.datetime.now().timestamp() - startTime < 1: # Checks the button for 1 second. For removing noise in signal.
                if not GPIO.input(btn_pin):
                    change = True
                    break
                else:
                    time.sleep(0.1)
            if change == False:
                btnState = True
                time.sleep(0.0001)
            else:
                change = False
                time.sleep(0.0001)
        else:
            btnState = False
        
        if btnState != lastBtnState:
            print("button pushed!")
            lastBtnState = btnState
            response = requests.get("http://localhost:3000/lightstate?toggle=change")
            print(response.text)

# When you press ctrl+c, this will be called
finally:
    GPIO.cleanup()
