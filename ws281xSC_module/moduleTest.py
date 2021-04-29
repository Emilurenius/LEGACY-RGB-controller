import ws281xSC

LEDs = ws281xSC.LEDs(149, "http://192.168.1.124:3000")

LEDs.setState(True)