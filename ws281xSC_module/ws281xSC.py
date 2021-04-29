# Library for controlling lights connected to the server in this repository
import requests

class LEDs:
    def __init__(self, LEDcount, address):
        self.LEDcount = LEDcount
        self.address = address
        self.LEDdata = {}
        i = 0
        while i < self.LEDcount:
            self.LEDdata[i] = {
                "br": 0,
                "r": 0,
                "g": 0,
                "b": 0,
            }
            i += 1
    
    def checkAddress(self): # For debugging
        return self.address

    def printLEDdata(self): # For debugging
        for key, value in self.LEDdata.items():
            print(key, value)

    def percentofLEDs(self, percentage):
        return int(self.LEDcount * percentage / 100)
    
    def setMode(self, mode):
        response = requests.get(f"{self.address}/modes/set?mode={mode}")
        return response

    def setPixelData(self, i, br=None, r=None, g=None, b=None):
        if br:
            self.LEDdata[i]["br"] = br
        if r:
            self.LEDdata[i]["r"] = r
        if g:
            self.LEDdata[i]["g"] = g
        if b:
            self.LEDdata[i]["b"] = b