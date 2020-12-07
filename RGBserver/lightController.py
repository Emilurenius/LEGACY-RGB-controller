#!/usr/bin/env python3 rpi_ws281x library strandtest example Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time, json, os, random
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def solidColor(strip, color, wait_ms=50):
    # Displays a single solid color untill told otherwise:
    for i in range(strip.numPixels()):
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

def theaterChase(strip, color, wait_ms=50, iterations=1):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        try:
            with open("./json/data.json") as JSON:
                data = json.load(JSON)
        except:
            print("JSON busy...")
        if data["onoff"] != True or data["mode"] != "theaterChase":
            break

        for q in range(3):
            try:
                with open("./json/data.json") as JSON:
                    data = json.load(JSON)
            except:
                print("JSON busy...")
            if data["onoff"] != True or data["mode"] != "theaterChase":
                break

            for i in range(0, strip.numPixels(), 3):
                try:
                    with open("./json/data.json") as JSON:
                        data = json.load(JSON)
                except:
                    print("JSON busy...")
                if data["onoff"] != True or data["mode"] != "theaterChase":
                    break

                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                try:
                    with open("./json/data.json") as JSON:
                        data = json.load(JSON)
                except:
                    print("JSON busy...")
                if data["onoff"] != True or data["mode"] != "theaterChase":
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

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    roundOne = True
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
            if roundOne == True:
                strip.show()
        roundOne = False
        strip.show()
        try:
            with open("./json/data.json") as JSON:
                data = json.load(JSON)
        except:
            print("JSON busy...")
        if data["onoff"] != True or data["mode"] != "rainbow":
            break
        time.sleep(wait_ms/1000.0)

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
    numberofRED = int(float(strip.numPixels()) * 0.3)
    numberofWHITE = int(float(strip.numPixels()) * 0.1)
    numberofBLUE = int(float(strip.numPixels()) * 0.2)
    total = numberofRED * 2 + numberofWHITE * 2 + numberofBLUE
    if total != strip.numPixels():
        numberofRED += (strip.numPixels() - total) / 2
    
    x = 0
    LED = 0
    while x < numberofRED:
        strip.setPixelColor(LED, Color(255, 0, 0))
        strip.show()
        x += 1
        LED += 1
    x = 0
    while x < numberofWHITE:
        strip.setPixelColor(LED, Color(255, 255, 255))
        strip.show()
        x += 1
        LED += 1
    x = 0
    while x < numberofBLUE:
        strip.setPixelColor(LED, Color(0, 0, 255))
        strip.show()
        x += 1
        LED += 1
    x = 0
    while x < numberofWHITE:
        strip.setPixelColor(LED, Color(255, 255, 255))
        strip.show()
        x += 1
        LED += 1
    x = 0
    while x < numberofRED:
        strip.setPixelColor(LED, Color(255, 0, 0))
        strip.show()
        x += 1
        LED += 1

def colorDrip(strip, wait_ms=50):
    # Colors drip in from the side, and collect in the end of the LED strip:
    steps = strip.numPixels()
    for i in range(strip.numPixels()):
        color1 = random.randint(0, 255)
        color2 = random.randint(0, 255)
        fullColor = random.randint(0, 2)

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

        x = 0
        while x < steps:
            strip.setPixelColor(x, Color(r, g, b))
            strip.show()
            time.sleep(wait_ms/1000.0)
            if x < steps -1:
                strip.setPixelColor(x, Color(0, 0, 0))
            x += 1
        
        steps -= 1

        if steps == 0:
            colorWipe(strip, Color(0, 0, 0))

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
        #colorDrip(strip)
        while True:
            norge(strip)
        #     try:
        #         with open("./json/data.json") as JSON:
        #             data = json.load(JSON)
        #     except:
        #         print("JSON busy...")
        #         time.sleep(0.05)

        #     if data["onoff"] and data["mode"] == "standard":
        #         colorWipe(strip, Color(data["R"], data["G"], data["B"]), 3)
        #     elif data["onoff"] and data["mode"] == "rainbow":
        #         rainbow(strip)
        #     elif data["onoff"] and data["mode"] == "theaterChase":
        #         theaterChase(strip, Color(data["R"], data["G"], data["B"]))
        #     elif data["onoff"] and data["mode"] == "norway":
        #         norge(strip)
        #     else:
        #         colorWipe(strip, Color(0, 0, 0), 3)

        #     print ('Color wipe animations.')
        #     colorWipe(strip, Color(255, 0, 0))  # Red wipe
        #     colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        #     colorWipe(strip, Color(0, 0, 255))  # Green wipe
        #     print ('Theater chase animations.')
        #     theaterChase(strip, Color(127, 127, 127))  # White theater chase
        #     theaterChase(strip, Color(127,   0,   0))  # Red theater chase
        #     theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
        #     print ('Rainbow animations.')
        #     rainbow(strip)
        #     rainbowCycle(strip)
        #     theaterChaseRainbow(strip)

    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 10)
