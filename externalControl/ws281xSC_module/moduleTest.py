import ws281xSC

strip = ws281xSC.strip(149, "http://172.16.4.195:3000") # Address will be different for you
strip.setMode("songAnimation")
strip.setState(True)