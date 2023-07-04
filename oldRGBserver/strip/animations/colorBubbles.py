class ColorBubbles:
    
    def __init__(self, args):

        self.name = 'colorBubbles'

        self.numPixels = args['numPixels']

        self.pixelData = {}

        for i in range(self.numPixels):
            self.pixelData[i] = {
                "val": 0,
                "up": True,
                "active": False
            }
    
    def animateFrame(self, speed, tLength, bDistance):

        if bDistance > self.numPixels() - 1:
            bDistance = self.numPixels() - 1

        noneActive = True
        for i in range(bDistance):
            if self.pixelData[i]["active"] == True:
                noneActive = False
                break
        if noneActive:
            self.pixelData[1]["active"] = True

        for i in range(len(self.pixelData)):
            # Fade up
            if self.pixelData[i]["up"] == True and self.pixelData[i]["val"] < 1000 and self.pixelData[i]["active"] == True:
                self.pixelData[i]["val"] += speed
                if self.pixelData[i]["val"] > 1000:
                    self.pixelData[i]["val"] = 1000

            # Fade down
            elif self.pixelData[i]["active"] == True and self.pixelData[i]["val"] > 0:
                self.pixelData[i]["up"] = False
                self.pixelData[i]["val"] -= speed/tLength
                if self.pixelData[i]["val"] < 0:
                    self.pixelData[i]["val"] = 0

            # Deactivate pixel
            else:
                self.pixelData[i]["active"] = False

            # Reset pixel
            if self.pixelData[i]["val"] == 0 and self.pixelData[i]["up"] == False:
                self.pixelData[i]["up"] = True
                self.pixelData[i]["active"] = False

            # Activate next pixel
            if self.pixelData[i]["val"] > 999 and i < len(self.pixelData) - 1:
                self.pixelData[i+1]["active"] = True

            color = Color(int(float(data["R"]) * float(self.pixelData[i]["val"]) / 1000), int(float(data["G"]) * float(self.pixelData[i]["val"]) / 1000), int(float(data["B"]) * float(self.pixelData[i]["val"]) / 1000))
            strip.setPixelColor(i, color)