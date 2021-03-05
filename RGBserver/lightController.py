# Based on the python3 rpi_ws281x library strandtest example made by: Tony DiCola (tony@tonydicola.com)
# The structure of the code, and many of the functions that animate the LEDs are taken directly from the strandtest example.
# I have made a lot of changes, like adding some of my own functions for animating the LED strip, and connecting the script to a JSON file.
# The JSON file tells the script how to animate the LEDs, and what color they should be when they are not being animated.
# Other information could also be passed through the JSON file. If you add your own data to the JSON file named data.json
# That data will be available in the dictionary variable called "data"

# The original example script that this script is built upon can be found in the same github repository as this file
# Or you can go to the original github repository here: https://github.com/jgarff/rpi_ws281x

import time, json, os, random, datetime, argparse, requests
from rpi_ws281x import *

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
        return False # If the JSON file can't be opened, just assume the lights should be on, and the mode hasn't changed

def getDataval(dataval):
    try: # Try opening the json file, and check it
        with open("./json/data.json") as JSON:
            data = json.load(JSON)
        return data[dataval]
    except: # If you can't open the json file, just return False
        return False

# Define functions which animate LEDs in various ways:
def randColor():
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
    RGB = {
        "r": r,
        "g": g,
        "b": b
    }
    return RGB

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def solidColor(strip, color):
    # Displays a single solid color untill told otherwise:
    for i in range(strip.numPixels()): # Assign color to every pixel
        strip.setPixelColor(i, color)
    strip.show()
    print("New solid color loaded")

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
            RGB = randColor()

            x = 0 # Set x to 0, this will be used to increment while loop underneath
            
            while x < steps: # Repeated for every LED in the strip

                # generate droplet with tail:
                strip.setPixelColor(x, Color(RGB["r"], RGB["g"], RGB["b"])) # main pixel
                strip.setPixelColor(x - 1, Color(int(float(RGB["r"]) * float(60 / 100)), int(float(RGB["g"]) * float(60 / 100)), int(float(RGB["b"]) * float(60 / 100)))) # Tail pixel 1
                strip.setPixelColor(x - 2, Color(int(float(RGB["r"]) * float(20 / 100)), int(float(RGB["g"]) * float(20 / 100)), int(float(RGB["b"]) * float(20 / 100)))) # Tail pixel 2
                strip.setPixelColor(x - 3, Color(int(float(RGB["r"]) * float(1 / 100)), int(float(RGB["g"]) * float(1 / 100)), int(float(RGB["b"]) * float(1 / 100)))) # Tail pixel 3
                strip.setPixelColor(x - 4, Color(0, 0, 0)) # Reset overflowing tail pixels
                strip.show()
                if getDataval("speed"): #Update speed for animation from JSON file
                    wait_ms = 100 - getDataval("speed")
                time.sleep(wait_ms/1000.0) # Wait for given time from JSON file

                if checkBreak("colorDrip"): # Stop function if the mode has changed, or the lights are turned off.
                    break
                x += 1

            # Remove tail when droplet stops:
            strip.setPixelColor(steps - 4, Color(0, 0, 0))
            strip.show()
            time.sleep(wait_ms/1000.0) # Wait for given time from JSON file
            strip.setPixelColor(steps - 3, Color(0, 0, 0))
            strip.show()
            time.sleep(wait_ms/1000.0) # Wait for given time from JSON file
            strip.setPixelColor(steps - 2, Color(0, 0, 0))
            strip.show()
            
            steps -= 1 # Remove one step before next increment. This makes sure the next animation stops right before the previous one, making the colors stack.

            if checkBreak("colorDrip"):
                break

            if steps == 0: # When all LEDs have been filled, colorWipe with black.
                colorWipe(strip, Color(0, 0, 0))

def alarmClock(strip):
    alarmDone = False
    while True:

        if alarmDone:
            break

        previousData = False
        try:
            with open("./json/data.json") as JSON: # Read data file
                data = json.load(JSON)
        except:
            time.sleep(0.05)
            continue

        if data["mode"] != "alarmClock": # Check if alarmClock mode is still on
            break # Break out of loop, and exit function if mode is not alarmClock

        currentTime = datetime.datetime.now() # save the current time as a datetime
        hour = currentTime.hour # Extract current hour from datetime
        minute = currentTime.minute # Extract current minute from datetime

         # Add 0 to front of hour and minute if they only have one digit
        if hour < 10:
            hour = "0" + str(hour)
        if minute < 10:
            minute = "0" + str(minute)

        currentTime_Formatted = str(hour) + ":" + str(minute) # Combine hour and minute into format
        alarmTime = data["alarmClockData"]["alarmTime"]

        if currentTime_Formatted == alarmTime: # Check if current time is the same as inputted alarm activation time
            if data["onoff"] == False:
                requests.get("http://localhost:3000/lightstate?toggle=change")

            while True: # This will run untill the user turns off the lights, or changes mode. Note that turning lights off and on will restart the alarmclock function.
                
                colorWipe(strip, Color(255, 255, 255), 0)
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                colorWipe(strip, Color(0, 0, 0), 0)
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break

                solidColor(strip, Color(255, 255, 255))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                time.sleep(0.3)
                solidColor(strip, Color(0, 0, 0))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                time.sleep(0.3)
                solidColor(strip, Color(255, 255, 255))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                time.sleep(0.3)
                solidColor(strip, Color(0, 0, 0))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                time.sleep(0.3)
                solidColor(strip, Color(255, 255, 255))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                time.sleep(0.3)
                solidColor(strip, Color(0, 0, 0))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                time.sleep(0.3)
                solidColor(strip, Color(255, 255, 255))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break
                time.sleep(0.3)
                solidColor(strip, Color(0, 0, 0))
                if checkBreak("alarmClock"): # Stop function if the mode has changed, or the lights are turned off.
                    alarmDone = True
                    break

        else: # If the alarm time has not been reached, act like standard mode.
            if previousData != data: 
                previousData = data
                if data["onoff"]:
                    colorWipe(strip, Color(int(float(data["R"]) * float(data["brightness"]) / 1000), int(float(data["G"]) * float(data["brightness"]) / 1000), int(float(data["B"]) * float(data["brightness"]) / 1000)), 3)
                else:
                    colorWipe(strip, Color(0, 0, 0), 3)

def elitus(strip, data):
    while True:
        if checkBreak("elitus"):
            break

        try:
            with open("./json/data.json") as JSON:
                data = json.load(JSON)
        except:
            time.sleep(0.05)

        if data["eliteData"]["mode"] == "standard":
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(255, 24, 0))
            strip.show()

        if data["eliteData"]["mode"] == "jump":
            startTime = datetime.datetime.now().timestamp()
            br = 100
            plus = False
            cancelAnimation = False
            while datetime.datetime.now().timestamp() - startTime < 20:
                print(br)
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(int(float(255) * float(br / 100)), int(float(24) * float(br / 100)), 0))
                strip.show()
                try:
                    with open("./json/data.json") as JSON:
                        data = json.load(JSON)
                        if data["eliteData"]["mode"] != "jump":
                            cancelAnimation = True
                            break
                except:
                    time.sleep(0.05)
                if checkBreak("elitus"):
                    break
                if plus:
                    br += 2
                else:
                    br -= 2
                if br < 1:
                    br = 1
                elif br > 100:
                    br = 100
                if br == 1:
                    plus = True
                elif br == 100:
                    plus = False

            startTime = datetime.datetime.now().timestamp()
            while datetime.datetime.now().timestamp() - startTime < 13:
                if cancelAnimation:
                    break
                RGB = randColor()
                
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(RGB["r"], RGB["g"], RGB["b"]))
                strip.show()
                if checkBreak("elitus"):
                    break
                time.sleep(0.05)

def colorBubbles(strip): 
    stripBrightness = {}

    for i in range(strip.numPixels()):
        stripBrightness[i + 1] = {
            "val": 0,
            "up": True,
            "active": False
        }
    
    while True:
        wait_ms = 100 - getDataval("speed")
        if checkBreak("colorBubbles"):
            break

        noneActive = True
        for i in range(len(stripBrightness)):
            if stripBrightness[i + 1]["active"] == True:
                noneActive = False
                break
        if noneActive:
            stripBrightness[1]["active"] = True

        for i in range(len(stripBrightness)):
            if stripBrightness[i + 1]["up"] == True and stripBrightness[i + 1]["val"] < 1000 and stripBrightness[i + 1]["active"] == True:
                stripBrightness[i + 1]["val"] += 400
                if stripBrightness[i + 1]["val"] > 1000:
                    stripBrightness[i + 1]["val"] = 1000

            elif stripBrightness[i + 1]["active"] == True and stripBrightness[i + 1]["val"] > 0:
                stripBrightness[i + 1]["up"] = False
                stripBrightness[i + 1]["val"] -= 100
                if stripBrightness[i + 1]["val"] < 0:
                    stripBrightness[i + 1]["val"] = 0

            else:
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] == 0 and stripBrightness[i + 1]["up"] == False:
                stripBrightness[i + 1]["up"] = True
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] > 999 and i < len(stripBrightness) - 1:
                stripBrightness[i + 2]["active"] = True

            color = Color(int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(255) * float(stripBrightness[i + 1]["val"]) / 1000))
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def bpm(strip):
    while True:
        if checkBreak("bpm"):
            break

        # Load BPM data to see how long to wait until the color is changed again.
        while True: # This goes in a loop until the JSON file can be loaded, or mode is changed
            try:
                with open("./json/bpm.json") as JSON: # Load BPM data saved to json file by server
                    rawBPMdata = json.load(JSON) # Load JSON file as a dictionary
                    BPM = rawBPMdata["value"] # Extract BPM value
                    waitTime = 60 / int(BPM) # Calculate wait time based on BPM
                    syncDelay = rawBPMdata["syncDelay"] # Check how long to wait for next beat in song
                    rawBPMdata["syncDelay"] = 0 # Reset delay before next loop
                    with open("./json/bpm.json", "w") as outFile: # Open json file for editing
                        json.dump(rawBPMdata, outFile) # Save delay change 
                    break
            except:
                if checkBreak("bpm"):
                    break

        while True: # Wait for next beat in song
            if syncDelay == 0:
                break # If there is no wait time, just carry on
            elif time.time() >= syncDelay:
                break # Break out of loop when the next beat comes
        
        RGB = randColor()
        solidColor(strip, Color(RGB["r"], RGB["g"], RGB["b"])) # Assign a random color to the whole light strip
        print("Changed color")

        startTime = time.time() # Save current seconds since 1.January 1970
        endTime = startTime + waitTime # Add wait time to startTime to get endTime
        while True:
            if time.time() >= endTime: # Stop looping when current time equals endTime
                break
            elif checkBreak("bpm"): # Stop looping if mode is changed
                break

            try:
                with open("./json/bpm.json") as JSON: # Load BPM data saved to json file by server
                    rawBPMdata = json.load(JSON) # Load JSON file as a dictionary
                    BPM = rawBPMdata["value"] # Extract BPM value
                    newWaitTime = 60 / float(BPM) # Calculate wait time based on BPM
                    new
                    
                    if newWaitTime != waitTime: # Stop waiting if the wait time is changed
                        waitTime = newWaitTime
                        break
            except:
                if checkBreak("bpm"):
                    break

def screenSync(strip):
    currentColor = None
    data = None
    R = None
    G = None
    B = None
    while True:
        if checkBreak("screenSync"):
            break
        
        while True:
            try:
                with open("./json/data.json") as JSON: # Load BPM data saved to json file by server
                    data = json.load(JSON) # Load JSON file as a dictionary
                    R = data["R"]
                    G = data["G"]
                    B = data["B"]
                    break
            except:
                if checkBreak("screenSync"):
                    break
        newColor = [R, G, B]

        if currentColor == None:
            currentColor = newColor
        elif currentColor == newColor:
            currentColor = newColor
        else:
            if currentColor[0] < newColor[0]: # Change red channel
                if newColor[0] - currentColor[0] < 5:
                    currentColor[0] += 5
                else:
                    currentColor[0] = currentColor[0] + newColor[0]
            else:
                if currentColor[0] - newColor[0] < 5:
                    currentColor[0] -= 5
                else:
                    currentColor[0] = currentColor[0] - newColor[0]
            
            if currentColor[1] < newColor[1]: # Change green channel
                if newColor[1] - currentColor[1] < 5:
                    currentColor[1] += 5
                else:
                    currentColor[1] = currentColor[1] + newColor[1]
            else:
                if currentColor[1] - newColor[1] < 5:
                    currentColor[1] -= 5
                else:
                    currentColor[1] = currentColor[1] - newColor[1]
                

            if currentColor[2] < newColor[2]: # Change blue channel
                if newColor[2] - currentColor[2] < 5:
                    currentColor[2] += 5
                else:
                    currentColor[2] = currentColor[2] + newColor[2]
            else:
                if currentColor[2] - newColor[2] < 5:
                    currentColor[2] -= 5
                else:
                    currentColor[2] = currentColor[2] - newColor[2]
                

        solidColor(strip, Color(currentColor[0], currentColor[1], currentColor[2]))


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
                time.sleep(0.05)
            
            if previousData != data:
                print("\nChecking mode")
                previousData = data
                # Checking what mode to run:
                if data["onoff"] and data["mode"] == "standard":
                    print("Standard / ColorWipe")
                    print("RGB:", data["R"], data["G"], data["B"])
                    print("Brightness:", data["brightness"] / 10, "%")
                    colorWipe(strip, Color(int(float(data["R"]) * float(data["brightness"]) / 1000), int(float(data["G"]) * float(data["brightness"]) / 1000), int(float(data["B"]) * float(data["brightness"]) / 1000)), 3)
                
                elif data["onoff"] and data["mode"] == "solidColor":
                    print("SolidColor")
                    print("RGB:", data["R"], data["G"], data["B"])
                    solidColor(strip, Color(int(float(data["R"]) * float(data["brightness"]) / 1000), int(float(data["G"]) * float(data["brightness"]) / 1000), int(float(data["B"]) * float(data["brightness"]) / 1000)))
                
                elif data["onoff"] and data["mode"] == "rainbow":
                    print("Rainbow")
                    rainbow(strip, 100 - data["speed"])
                
                elif data["onoff"] and data["mode"] == "theaterChase":
                    print("Theater chase")
                    theaterChase(strip, Color(data["R"], data["G"], data["B"]), 100 - data["speed"])
                
                elif data["onoff"] and data["mode"] == "norway":
                    print("NORWAY!")
                    norge(strip)
                
                elif data["onoff"] and data["mode"] == "colorDrip":
                    print("Color drip")
                    colorDrip(strip, 100 - data["speed"])
                
                elif data["onoff"] and data["mode"] == "alarmClock":
                    print("Alarm clock")
                    print("Waking up at:", data["alarmClockData"]["alarmTime"])
                    alarmClock(strip)
                
                elif data["onoff"] and data["mode"] == "elitus":
                    print("Elitus mode")
                    elitus(strip, data)

                elif data["onoff"] and data["mode"] == "colorBubbles":
                    print("Color bubbles")
                    colorBubbles(strip)

                elif data["onoff"] and data["mode"] == "bpm":
                    print("bpm activated")
                    bpm(strip)

                elif data["onoff"] and data["mode"] == "screenSync":
                    print("Screen syncing activated")
                    screenSync(strip)
                
                else:
                    print("Lights off")
                    colorWipe(strip, Color(0, 0, 0), 3)
            else:
                time.sleep(0.5)

    except KeyboardInterrupt: # This makes sure the RGB strip turns off when you close the script
        colorWipe(strip, Color(0,0,0), 10)