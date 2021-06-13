import ws281xSC, time
from datetime import datetime

strip = ws281xSC.strip(149, "http://192.168.1.124:3000")
strip.setMode("directRGB")

r = 0
g = 0
b = 0
while True:
    total = r+g+b
    dividedTotal = total/765
    percentageDone = dividedTotal * 100
    print(r, g, b, percentageDone, "%")
    r+=1

    if r > 255:
        r = 0
        g+=1

    if g > 255:
        g = 0
        b+=255

    if b > 255:
        time.sleep(1)
        break

    i = 0
    while i < strip.LEDcount:
        strip.setPixelData(i, r, g, b)
        i+=1
    strip.show()