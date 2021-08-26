import ws281xSC

strip = ws281xSC.strip(149, "http://192.168.1.124:3000") # Address will be different for you
strip.setMode("directRGB")

strip.setMode("standard")
strip.setState(True)