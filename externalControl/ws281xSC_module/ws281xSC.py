# Library for controlling lights connected to the server in this repository
import requests, copy

class strip:
    def __init__(self, LEDcount, address):
        self.LEDcount = LEDcount
        self.address = address
        self.LEDdata = {}
        i = 0
        while i < self.LEDcount:
            self.LEDdata[i] = [0, 0, 0]
            i += 1
        self.prevLEDdata = copy.deepcopy(self.LEDdata)
    
    def checkAddress(self): # For debugging
        return self.address

    def printLEDdata(self): # For debugging
        for key, value in self.LEDdata.items():
            print(key, value)

    def percentofLEDs(self, percentage): # Returns amount of LEDs in given percentage
        return int(self.LEDcount * percentage / 100)

    def getJSON(self, fileName): # Returns requested json file from RGB server
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

    def setPixelData(self, i, r=None, g=None, b=None):
        if r != None:
            self.LEDdata[i][0] = r
        if g != None:
            self.LEDdata[i][1] = g
        if b != None:
            self.LEDdata[i][2] = b

    def show(self, onlyChanged=False):
        # Commented out code doesn't register a change from color to no color for some reason.
        # changedData = {}
        # for k, v in self.LEDdata.items():
        #     if self.LEDdata[k] != self.prevLEDdata[k]:
        #         changedData[k] = self.LEDdata[k]

        # requests.post(f"{self.address}/directRGB", changedData)

        requests.post(f"{self.address}/directRGB", self.LEDdata)