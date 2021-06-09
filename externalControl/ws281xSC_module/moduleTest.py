import ws281xSC, time
from datetime import datetime

LEDs = ws281xSC.LEDs(149, "http://192.168.1.124:3000")

i = 0
prevLED = None
while True:
    start = datetime.now()
    LEDs.setPixelData(i, 255, 0, 0)
    if prevLED != None:
        LEDs.setPixelData(prevLED, 0, 0, 0)
    prevLED = i
    i +=1

    if i > LEDs.LEDcount - 1:
        i = 0

    LEDs.show()
    print(datetime.now() - start)
