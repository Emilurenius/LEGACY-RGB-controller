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

    def percentofLEDs(self, percentage): # Returns amount of LEDs in given percentage
        return int(self.LEDcount * percentage / 100)

    def getJSON(self, fileName):
        while True:
            try:
                return requests.get(f"{self.address}/json/{fileName}").json()
            except:
                continue
    
    def setMode(self, mode): # Will set the mode of the lightController to given string
        response = requests.get(f"{self.address}/modes/set?mode={mode}")
        return response

    def setState(self, state=None): # Used to turn lights on and off. Can either give it desired state, or give nothing to toggle.
        if state == None:
            requests.get(f"{self.address}/lightstate?toggle=change")
        else:
            if requests.get(f"{self.address}/lightstate").json() == state:
                print("Already", state)
            else:
                requests.get(f"{self.address}/lightstate?toggle=change")

    def setPixelData(self, i, br=None, r=None, g=None, b=None):
        if br:
            self.LEDdata[i]["br"] = br
        if r:
            self.LEDdata[i]["r"] = r
        if g:
            self.LEDdata[i]["g"] = g
        if b:
            self.LEDdata[i]["b"] = b