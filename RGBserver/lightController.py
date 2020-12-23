# Based on the python3 rpi_ws281x library strandtest example made by: Tony DiCola (tony@tonydicola.com)
# The structure of the code, and many of the functions that animate the LEDs are taken directly from the strandtest example.
# I have made a lot of changes, like adding some of my own functions for animating the LED strip, and connecting the script to a JSON file.
# The JSON file tells the script how to animate the LEDs, and what color they should be when they are not being animated.
# Other information could also be passed through the JSON file. If you add your own data to the JSON file named data.json
# That data will be available in the dictionary variable called "data"

# The original example script that this script is built upon can be found in the same github repository as this file
# Or you can go to the original github repository here: https://github.com/jgarff/rpi_ws281x

import time, json, os, random, datetime
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 149      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


# A check to see if a mode is still chosen. 
# will return False if the mode given to the function is the same as the one currently chosen on the web interface, or if there is an error loading the JSON file.
# Will return True if the mode given to the function is not the same as the one currently chosen on the web interface.
def checkBreak(mode):
    try: # Try opening the json file, and check it
        with open("./json/data.json") as JSON:
            data = json.load(JSON)
        if data["onoff"] != True or data["mode"] != mode: # Check if the mode has changed, and if the lights should be on
            return True # Return True if lights should be off, or the mode has changed
        else:
            return False # Return False if lights should be on, and the mode has not changed
    except: # If you can't open the json file, just return False
        print("JSON busy...")
        return False # If the JSON file can't be opened, just assume the lights should be on, and the mode hasn't changed

def getDataval(dataval):
    try: # Try opening the json file, and check it
        with open("./json/data.json") as JSON:
            data = json.load(JSON)
        return data[dataval]
    except: # If you can't open the json file, just return False
        print("JSON busy...")
        return False

# Define functions which animate LEDs in various ways:
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def solidColor(strip, color, wait_ms=50):
    # Displays a single solid color untill told otherwise:
    for i in range(strip.numPixels()): # Assign color to every pixel
        strip.setPixelColor(i, color)
    strip.show()

def starryNight(strip, wait_ms=50):
    # Fades on and off one random LED at a time:
    LED = random.randint(0, 148)
    
    x = 0
    while x <= 254:
        strip.setPixelColor(LED, Color(x, x, x))
        strip.show()
        x += 1
        print(LED, x)
        time.sleep(wait_ms/1000.0)
    
    while x >= 0:
        strip.setPixelColor(LED, Color(x, x, x))
        strip.show()
        x -= 1
        print(LED, x)
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50):
    """Movie theater light style chaser animation."""

    while True:
        newSpeed = getDataval("speed")
        if newSpeed:
            wait_ms = 100 - newSpeed # Making sure the speed stays up to date with JSON file.

        if checkBreak("theaterChase"): # Stop function if the mode has changed, or the lights are turned off.
            break
        for q in range(3):
            if checkBreak("theaterChase"):
                break

            for i in range(0, strip.numPixels(), 3):
                if checkBreak("theaterChase"):
                    break

                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                if checkBreak("theaterChase"):
                    break
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20):
    """Draw rainbow that fades across all pixels at once."""
    roundOne = True
    while True:
        if checkBreak("rainbow"): # Stop function if the mode has changed, or the lights are turned off.
            break
        
        for j in range(256):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, wheel((i+j) & 255))
                if roundOne == True:
                    strip.show()
            roundOne = False
            strip.show()
            newSpeed = getDataval("speed")
            if newSpeed:
                wait_ms = 100 - newSpeed # Making sure the speed stays up to date with JSON file.
            time.sleep(wait_ms/1000.0)

            if checkBreak("rainbow"):
                break

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def norge(strip, wait_ms=50):
    # Makes the color strip create the norwegian flag!

    # Calculate number of LEDs for every color in the flag based on the amount of LEDs being controlled.
    # This makes the script compatible with any length of LED strip.
    numberofRED = int(float(strip.numPixels()) * 0.3) # Calculate number of red LEDs on both sides of the flag
    numberofWHITE = int(float(strip.numPixels()) * 0.1) # Calculate number of white LEDs on both sides of the flag
    numberofBLUE = int(float(strip.numPixels()) * 0.2) # Calculate number of blue LEDs in the middle of the flag
    total = numberofRED * 2 + numberofWHITE * 2 + numberofBLUE
    if total != strip.numPixels():
        numberofRED += (strip.numPixels() - total) / 2
    
    x = 0 # Value for incrementing
    LED = 0 # Set start value for first LED to be animated. This should always be 0
    # Notice that LED does not get reset for every color like x does. That is why x and LED are different variables.
    while x < numberofRED: # Repeat for amount of red per side calculated
        strip.setPixelColor(LED, Color(255, 0, 0))
        strip.show()
        x += 1
        LED += 1
    x = 0 # Reset increment for next color
    while x < numberofWHITE: # Repeat for amount of white per side calculated
        strip.setPixelColor(LED, Color(255, 255, 255))
        strip.show()
        x += 1
        LED += 1
    x = 0 # Reset increment for next color
    while x < numberofBLUE: # Repeat for amount of blue calculated
        strip.setPixelColor(LED, Color(0, 0, 255))
        strip.show()
        x += 1
        LED += 1
    x = 0 # Reset increment for next color
    while x < numberofWHITE: # Repeat for amount of white per side calculated
        strip.setPixelColor(LED, Color(255, 255, 255))
        strip.show()
        x += 1
        LED += 1
    x = 0 # Reset increment for next color
    while x < numberofRED: 
        strip.setPixelColor(LED, Color(255, 0, 0))
        strip.show()
        x += 1
        LED += 1

def colorDrip(strip, wait_ms=50):
    # Colors drip in from the side, and collect in the end of the LED strip:
    
    while True:
        if checkBreak("colorDrip"): # Stop function if the mode has changed, or the lights are turned off.
            break
        steps = strip.numPixels() # Set steps for while Loop underneath to the amount of LEDs in the LED strip
        
        for i in range(strip.numPixels()): # Do this once for every LED in the light strip
            color1 = random.randint(0, 255) # Random color 1
            color2 = random.randint(0, 255) # Random color 2
            fullColor = random.randint(0, 2) # Choose one of the three RGB channels to be full brightness

            # The RGB channel chosen to be full brightness is set to 255, the others get assigned color1 and color2, wich are randomly generated
            if fullColor == 0:
                r = 255
                g = color1
                b = color2
            elif fullColor == 1:
                r = color1
                g = 255
                b = color2
            elif fullColor == 2:
                r = color1
                g = color2
                b = 255

            x = 0 # Set x to 0, this will be used to increment while loop underneath
            
            while x < steps: # Repeated for every LED in the strip
                strip.setPixelColor(x, Color(r, g, b))
                strip.setPixelColor(x - 1, Color(0, 0, 0))
                strip.show()
                if getDataval("speed"): #Update speed for animation from JSON file
                    wait_ms = 100 - getDataval("speed")
                time.sleep(wait_ms/1000.0) # Wait for given time from JSON file

                if checkBreak("colorDrip"): # Stop function if the mode has changed, or the lights are turned off.
                    break
                x += 1
            
            steps -= 1 # Remove one step before next increment. This makes sure the next animation stops right before the previous one, making the colors stack.

            if checkBreak("colorDrip"):
                break

            if steps == 0: # When all LEDs have been filled, colorWipe with black.
                colorWipe(strip, Color(0, 0, 0))

def alarmClock(strip, alarmTime, wait_ms=50):
    colorWipe(strip, Color(0, 0, 0), 3)

    while True: # Run time check forever

        if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
            break

        currentTime = datetime.datetime.now() # save the current time as a datetime
        hour = currentTime.hour # Extract current hour from datetime
        minute = currentTime.minute # Extract current minute from datetime

        # Add 0 to front of hour and minute if they only have one digit
        if hour < 10:
            hour = "0" + str(hour)
        if minute < 10:
            minute = "0" + str(minute)

        currentTime_Formatted = str(hour) + ":" + str(minute) # Combine hour and minute into format

        if currentTime_Formatted == alarmTime: # Check if current time is the same as inputted alarm activation time
            lightState = False
            while True: # This will run untill the user turns off the lights, or changes mode. Note that turning lights off and on will restart the alarmclock function.
                
                if lightState == False: # If just turned off, turn it on
                    if checkBreak("alarmClock"):
                        break
                    colorWipe(strip, Color(255, 255, 255), wait_ms)
                    lightState = True
                else: # If light just turned on, turn it off
                    if checkBreak("alarmClock"):
                        break
                    colorWipe(strip, Color(0, 0, 0), wait_ms)
                    lightState = False
                strip.show()

def elitus(strip, data):
    while True:
        if checkBreak("elitus"):
            break

        try:
            with open(dataFilePath) as JSON:
                data = json.load(JSON)
        except:
            print("JSON busy...")
            time.sleep(0.05)

        if data.eliteData.mode == "standard":
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, 255, 24, 0)
            strip.show()

        if data.eliteData.mode == "jump":
            startTime = datetime.datetime.now().timestamp()
            br = 1.0
            plus = False
            while datetime.datetime.now().timestamp() - startTime < 20:
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, int(float(255) * br), int(float(24) * br), 0)
                strip.show()
                if plus:
                    br += 0.01
                else:
                    br -= 0.01
                if br == 0.0:
                    plus = True
                elif br == 1.0:
                    plus = False


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        previousData = False
        while True:
            # Import data file:
            try:
                with open("./json/data.json") as JSON:
                    data = json.load(JSON)
            except:
                print("JSON busy...")
                time.sleep(0.05)
            
            if previousData != data:
                print("Checking mode")
                previousData = data
                # Checking what mode to run:
                if data["onoff"] and data["mode"] == "standard":
                    colorWipe(strip, Color(int(float(data["R"]) * float(data["brightness"]) / 1000), int(float(data["G"]) * float(data["brightness"]) / 1000), int(float(data["B"]) * float(data["brightness"]) / 1000)), 3)
                elif data["onoff"] and data["mode"] == "solidColor":
                    solidColor(strip, Color(int(float(data["R"]) * float(data["brightness"]) / 100), int(float(data["G"]) * float(data["brightness"]) / 100), int(float(data["B"]) * float(data["brightness"]) / 100)))
                elif data["onoff"] and data["mode"] == "rainbow":
                    rainbow(strip, 100 - data["speed"])
                elif data["onoff"] and data["mode"] == "theaterChase":
                    theaterChase(strip, Color(data["R"], data["G"], data["B"]), 100 - data["speed"])
                elif data["onoff"] and data["mode"] == "norway":
                    norge(strip)
                elif data["onoff"] and data["mode"] == "colorDrip":
                    colorDrip(strip, 100 - data["speed"])
                elif data["onoff"] and data["mode"] == "alarmClock":
                    alarmClock(strip, data["alarmClockData"]["alarmTime"], 100 - data["speed"])
                elif data["onoff"] and data["mode"] == "elitus":
                    elitus(strip, data)
                else:
                    colorWipe(strip, Color(0, 0, 0), 3)
            else:
                time.sleep(0.5)

    except KeyboardInterrupt: # This makes sure the RGB strip turns off when you close the script
        colorWipe(strip, Color(0,0,0), 10)
