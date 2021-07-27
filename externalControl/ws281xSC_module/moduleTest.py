import ws281xSC, time, progressbar
from datetime import datetime

strip = ws281xSC.strip(149, "http://192.168.1.124:3000")
strip.setMode("directRGB")

r = 0
g = 0
b = 0

strip.setMode("directRGB")
strip.show()