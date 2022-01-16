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
serverAddress = "http://localhost:3000"


def checkBreak(mode):
    # A check to see if a mode is still chosen. 
    # will return False if the mode given to the function is the same as the one currently chosen on the web interface.
    # Will return True if the mode given to the function is not the same as the one currently chosen on the web interface.
    data = getJSON("data")
    if data["onoff"] != True or data["mode"] != mode: # Check if the mode has changed, and if the lights should be on
        return True
    else:
        return False

def getJSON(filename):
    triesCounter = 0
     while True:
        try: # Try opening the json file, and check it
            # with open(f'./json/{filename}.json', 'r') as JSON:
            #     data = json.load(JSON)
            # return data
            file = open(f'./json/{filename}.json')
            data = json.load(file)
            file.close()
            return data
        except Exception as ex: # If you can't open the json file, just try again
            if triesCounter > 100:
                print(f'Exception has happened {triesCounter} times. Stopping script!')
                raise Exception(ex)
            else:
                print(f'Exception has happened {triesCounter} times')
                triesCounter += 1
                continue

def getDataval(dataval):
    data = getJSON("data")
    return data[dataval]

def unpackRGB(color): # Change 24 bit color into 8 bit RGB
    r = 0xFF & (color >> 16)
    g = 0xFF & (color >> 8)
    b = 0xFF & color
    return [r, g, b]

def timePrint(printVal, newLine=False):
    if newLine:
        print("\n")
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    print(f"{currentTime}: {printVal}")

def clamp(val, maxVal, minVal):
    if val < maxVal and val > minVal:
        return val
    elif val > maxVal:
        return maxVal
    elif val < minVal:
        return minVal
    else:
        return val

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
        "R": r,
        "G": g,
        "B": b
    }
    #timePrint(f"Random color generated: {RGB}")
    return RGB

def standard(strip, colorOverride=None):
    timePrint("Standard mode activated:", newLine=True)
    data = getJSON("data")
    standardSettings = getJSON("standardSettings")

    if standardSettings["colorChange"] == "wipe":
        if colorOverride:
            timePrint("Color overridden")
            R = colorOverride[0]
            G = colorOverride[1]
            B = colorOverride[2]
        else:
            R = int(float(data["R"]) * float(data["brightness"]) / 1000)
            G = int(float(data["G"]) * float(data["brightness"]) / 1000)
            B = int(float(data["B"]) * float(data["brightness"]) / 1000)

        timePrint(f"Wiping color to: {[R,G,B]}")
        colorWipe(strip, Color(R,G,B))
    
    elif standardSettings["colorChange"] == "fade":
        if colorOverride:
            timePrint("Color overridden")
            R = colorOverride[0]
            G = colorOverride[1]
            B = colorOverride[2]
        else:
            R = int(float(data["R"]) * float(data["brightness"]) / 1000)
            G = int(float(data["G"]) * float(data["brightness"]) / 1000)
            B = int(float(data["B"]) * float(data["brightness"]) / 1000)

        timePrint(f"Fading color to: {[R,G,B]}")
        fadeColor(strip, [R,G,B])

def colorWipe(strip, color, wait_ms=3):
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

def fadeColor(strip, newColor, wait_ms=10, changePerTick=1):
    oldColor = unpackRGB(strip.getPixelColor(0))
    while True:
        if newColor == oldColor:
            break

        if oldColor[0] == newColor[0]: # Change red channel
            oldColor[0] = newColor[0]
        elif oldColor[0] < newColor[0]:
            oldColor[0] += changePerTick
        elif oldColor[0] > newColor[0]:
            oldColor[0] -= changePerTick
        
        if oldColor[1] == newColor[1]: # Change green channel
            oldColor[1] = newColor[1]
        elif oldColor[1] < newColor[1]:
            oldColor[1] += changePerTick
        elif oldColor[1] > newColor[1]:
            oldColor[1] -= changePerTick
            
        if oldColor[2] == newColor[2]: # Change blue channel
            oldColor[2] = newColor[2]
        elif oldColor[2] < newColor[2]:
            oldColor[2] += changePerTick
        elif oldColor[2] > newColor[2]:
            oldColor[2] -= changePerTick

        solidColor(strip, Color(oldColor[0], oldColor[1], oldColor[2]))
        time.sleep(wait_ms / 1000) # Wait specified amount in delayMS

def starryNight(strip, wait_ms=50):
    # Fades on and off one random LED at a time:
    LED = random.randint(0, 148)
    
    x = 0
    while x <= 254:
        strip.setPixelColor(LED, Color(x, x, x))
        strip.show()
        x += 1
        timePrint(LED, x)
        time.sleep(wait_ms/1000.0)
    
    while x >= 0:
        strip.setPixelColor(LED, Color(x, x, x))
        strip.show()
        x -= 1
        timePrint(LED, x)
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, wait_ms=50):
    """Movie theater light style chaser animation."""
    timePrint("Theater chase activated", newLine=True)

    while True:
        data = getJSON("data")

        color = Color(data["R"], data["G"], data["B"])

        wait_ms = 100 - data["speed"] # Making sure the speed stays up to date with JSON file.

        for q in range(3):

            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            timePrint(wait_ms)
            if checkBreak("theaterChase"):
                    return
            for i in range(0, strip.numPixels(), 3):
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
    timePrint("Rainbow mode activated", newLine=True)
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
    timePrint("Norwegian flag being displayed", newLine=True)

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
    timePrint("Color drip activated", newLine=True)
    while True:
        if checkBreak("colorDrip"): # Stop function if the mode has changed, or the lights are turned off.
            break
        steps = strip.numPixels() # Set steps for while Loop underneath to the amount of LEDs in the LED strip
        
        for i in range(strip.numPixels()): # Do this once for every LED in the light strip
            RGB = randColor()

            x = 0 # Set x to 0, this will be used to increment while loop underneath
            
            while x < steps: # Repeated for every LED in the strip

                # generate droplet with tail:
                strip.setPixelColor(x, Color(RGB["R"], RGB["G"], RGB["B"])) # main pixel
                strip.setPixelColor(x - 1, Color(int(float(RGB["R"]) * float(60 / 100)), int(float(RGB["G"]) * float(60 / 100)), int(float(RGB["B"]) * float(60 / 100)))) # Tail pixel 1
                strip.setPixelColor(x - 2, Color(int(float(RGB["R"]) * float(20 / 100)), int(float(RGB["G"]) * float(20 / 100)), int(float(RGB["B"]) * float(20 / 100)))) # Tail pixel 2
                strip.setPixelColor(x - 3, Color(int(float(RGB["R"]) * float(1 / 100)), int(float(RGB["G"]) * float(1 / 100)), int(float(RGB["B"]) * float(1 / 100)))) # Tail pixel 3
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
    timePrint("Alarm clock mode activated", newLine=True)
    alarmDone = False
    previousData = False
    while True:

        if alarmDone:
            break

        data = getJSON("data")

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
            if previousData != data and data["onoff"]:
                previousData = data
                standard(strip)
            elif previousData != data and not data["onoff"]:
                previousData = data
                standard(strip, [0,0,0])

def alarmClockEC(strip): # Externally controlled alarm clock

    i = 0
    state = False
    while True: # This will run untill the user turns off the lights, or changes mode. Note that turning lights off and on will restart the alarmclock function.
                
        if checkBreak("alarmClockEC"): # Stop function if the mode has changed, or the lights are turned off.
            break

        if i == 0:
            colorWipe(strip, Color(255, 255, 255), 0)
        elif i == 1:
            colorWipe(strip, Color(0, 0, 0), 0)
        elif i == 10:
            i = -1 # Go one under 0, so it is 0 after adding 1 to index before next loop.
        else:
            if state:
                solidColor(strip, Color(0, 0, 0))
                state = False
                time.sleep(0.3)
            else:
                solidColor(strip, Color(255, 255, 255))
                state = True
                time.sleep(0.1)
        i += 1
    
    requests.get("http://localhost:3000/modes/set?mode=standard") # This practically breaks the loop through the checkBreak function, and changes to standard mode.

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
                timePrint(br)
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
        data = getJSON("data")
        if checkBreak("colorBubbles"):
            return

        noneActive = True
        for i in range(len(stripBrightness)):
            if stripBrightness[i + 1]["active"] == True:
                noneActive = False
                break
        if noneActive:
            stripBrightness[1]["active"] = True

        for i in range(len(stripBrightness)):
            # Fade up
            if stripBrightness[i + 1]["up"] == True and stripBrightness[i + 1]["val"] < 1000 and stripBrightness[i + 1]["active"] == True:
                stripBrightness[i + 1]["val"] += 400
                if stripBrightness[i + 1]["val"] > 1000:
                    stripBrightness[i + 1]["val"] = 1000

            # Fade down
            elif stripBrightness[i + 1]["active"] == True and stripBrightness[i + 1]["val"] > 0:
                stripBrightness[i + 1]["up"] = False
                stripBrightness[i + 1]["val"] -= 100
                if stripBrightness[i + 1]["val"] < 0:
                    stripBrightness[i + 1]["val"] = 0

            else: # Deactivate pixel
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] == 0 and stripBrightness[i + 1]["up"] == False: # Reset pixel
                stripBrightness[i + 1]["up"] = True
                stripBrightness[i + 1]["active"] = False

            if stripBrightness[i + 1]["val"] > 999 and i < len(stripBrightness) - 1: # Activate next pixel
                stripBrightness[i + 2]["active"] = True

            color = Color(int(float(data["R"]) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(data["G"]) * float(stripBrightness[i + 1]["val"]) / 1000), int(float(data["B"]) * float(stripBrightness[i + 1]["val"]) / 1000))
            strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def pulsate(strip, RGB):

    changePerMS = 15
    brightness = 0
    #goingUP = True

    # while True:

    #     if goingUP:
    #         brightness += changePerMS
    #     else:
    #         brightness -= changePerMS

    #     if brightness >= 255:
    #         goingUP = False
    #     elif brightness <= 0:
    #         solidColor(strip, Color(0,0,0)) # Make sure the strip goes black after animation
    #         break

    brightness = 400
    while True:
        brightness -= changePerMS

        if brightness <= 0:
            solidColor(strip, Color(0,0,0)) # Make sure the strip goes black after animation
            break

        R = int(float(RGB["R"]) * float(brightness) / 1000)
        G = int(float(RGB["G"]) * float(brightness) / 1000)
        B = int(float(RGB["B"]) * float(brightness) / 1000)

        solidColor(strip, Color(R,G,B))

        time.sleep(0.001)

def reactiveSync(strip, RGB):
    SA = requests.get(f"{serverAddress}/spotify/getAnalysis").json() # Get song analysis of currently playing song
    timePrint(SA["body"]["bars"][0])

def bpm(strip): # [0,150,255], [170, 0, 255]
    timePrint("BPM mode activated", newLine=True)
    # colorList = [
    #         {
    #             "R": 0,
    #             "G": 150,
    #             "B": 255
    #         },
    #         {
    #             "R": 170,
    #             "G": 0,
    #             "B": 255
    #         }
    #     ]
    colorIndex = 0
    while True:
        colorList = getJSON("presets") # Temp code
        keyList = list(colorList.keys()) # Extract keys for easy iteration later
        if checkBreak("bpm"):
            return

        rawBPMdata = getJSON("bpm") # Load JSON file as a dictionary
        bpmSettings = getJSON("bpmSettings") # Load settings

        # Extract needed data from server:
        doneAt = rawBPMdata["doneAt"] # Unix timestamp of when the currently synced song ends. Set to 0 if no song is synced.
        BPM = rawBPMdata["value"] # Extract BPM value

        # Check if synced spotify song is done, and if so, tell the server to refresh it's data:
        try:
            if float(doneAt)/1000 + 1 <= time.time() and int(doneAt) != 0: # Check if song is done, or if there was a song synced at all
                res = requests.get(f"{serverAddress}/spotify/getBPM")
                print("Requested new song data")
                if res.status_code == 400:
                    print("No song data recieved")
                    requests.get(f"{serverAddress}/bpm?mode=updateBPM&bpm={float(BPM)}") # This resets doneAt to 0, making sure the code doesn't just loop back here.
                    break
                continue
        except:
            pass

        # Sync with beat in song:
        waitTime = 60 / float(BPM) # Calculate wait time based on BPM
        syncDelay = rawBPMdata["syncDelay"] # Check how long to wait for next beat in song
        requests.get(f"{serverAddress}/bpm?mode=resetDelay")
        while syncDelay != 0: # Wait for next beat in song
            if time.time() >= syncDelay:
                break # Break out of loop when the next beat comes

        startTime = time.time() # Save timestamp for waiting for next beat later.
        
        # RGB = randColor() # Color to be used in selected animation

        RGB = colorList[keyList[colorIndex]]
        colorIndex += 1
        if colorIndex > len(colorList) - 1:
            colorIndex = 0
        print(RGB)
        
        delayActive = False
        if bpmSettings["animationType"] == "solid":
            solidColor(strip, Color(int(RGB["R"]), int(RGB["G"]), int(RGB["B"]))) # Assign a random color to the whole light strip
            delayActive = True
        elif bpmSettings["animationType"] == "pulsate":
            pulsate(strip, RGB)
            delayActive = True
        elif bpmSettings["animationType"] == "reactive":
            reactiveSync(strip, RGB)

        if delayActive:
            # Wait for next beat, without halting the script completely:
            endTime = startTime + waitTime # Add wait time to startTime to get endTime
            while True:
                if time.time() >= endTime: # Stop looping when current time equals endTime
                    break
                elif checkBreak("bpm"): # Stop looping if mode is changed
                    return

def screenSync(strip):
    currentColor = None
    data = None
    R = None
    G = None
    B = None
    changePerTick = 1
    delayMS = 30

    while True:
        if checkBreak("screenSync"):
            break
        
        data = getJSON("data") # Load JSON file as a dictionary
        R = data["R"]
        G = data["G"]
        B = data["B"]
        newColor = [R, G, B]

        if currentColor == None: # Set the value of the current color on the first round
            currentColor = newColor

        diffR = abs(newColor[0] - currentColor[0])
        diffG = abs(newColor[1] - currentColor[1])
        diffB = abs(newColor[2] - currentColor[2])
        diff = diffR+diffG+diffB/3*4 # Get average, and double
        diff = clamp(diff, 255, 0)
        delayMS = (255 - diff) / 4

        if currentColor[0] < newColor[0]: # Change red channel
            currentColor[0] += changePerTick
        elif currentColor[0] > newColor[0]:
            currentColor[0] -= changePerTick
        
        if currentColor[1] < newColor[1]: # Change green channel
            currentColor[1] += changePerTick
        elif currentColor[1] > newColor[1]:
            currentColor[1] -= changePerTick
            

        if currentColor[2] < newColor[2]: # Change blue channel
            currentColor[2] += changePerTick
        elif currentColor[2] > newColor[2]:
            currentColor[2] -= changePerTick

        # Make sure RGB values are not negative. That would cause a crash. 
        if currentColor[0] < 0:
            currentColor[0] = 0
        if currentColor[1] < 0:
            currentColor[1] = 0
        if currentColor[2] < 0:
            currentColor[2] = 0

        timePrint(currentColor)
        solidColor(strip, Color(currentColor[0], currentColor[1], currentColor[2])) # Set the RGB strip to the new color generated
        time.sleep(delayMS / 1000) # Wait specified amount in delayMS

def directRGB(strip):
    while True:
        if checkBreak("directRGB"):
            break
        rgbData = getJSON("directRGB")

        for k, v in rgbData.items():
            strip.setPixelColor(int(k), Color(int(v[0]), int(v[1]), int(v[2])))
        strip.show()

# This is the dictionary of all valid modes, and their accompanying function call:
modes = {
    "standard": standard,
    "solidColor": solidColor,
    "rainbow": rainbow,
    "theaterChase": theaterChase,
    "norway": norge,
    "colorDrip": colorDrip,
    "alarmClock": alarmClock,
    "alarmClockEC": alarmClockEC,
    "elitus": elitus,
    "colorBubbles": colorBubbles,
    "bpm": bpm,
    "screenSync": screenSync,
    "directRGB": directRGB
}

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
        previousData = None
        while True:
            data = getJSON("data")
            
            if previousData != data and data["onoff"]:
                previousData = data
                mode = modes.get(data["mode"], None)
                if mode:
                    mode(strip)
                else:
                    timePrint("Invalid mode", newLine=True)
            elif previousData != data and not data["onoff"]:
                previousData = data
                standard(strip, [0,0,0])

    except KeyboardInterrupt: # This makes sure the RGB strip turns off when you close the script
        standard(strip, [0,0,0])