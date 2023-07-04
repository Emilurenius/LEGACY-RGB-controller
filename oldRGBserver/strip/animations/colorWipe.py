import time

class ColorWipe:

    def __init__(self, args):

        self.numPixels = args['numPixels']

        if 'color' in args.keys():
            self.color = args['color']
        else:
            self.color = [255,255,255]
        
        self.speed = args['speed']

        self.pixelData = {}

        self.reset()

    def animateFrame(self):

        noneActive = True
        for i in range(self.numPixels):
            if self.pixelData[i]["active"] == True:
                noneActive = False
                break
        if noneActive:
            self.pixelData[0]["active"] = True

        for i in range(len(self.pixelData)):
            # Fade up
            if self.pixelData[i]["active"] == True and self.pixelData[i]['val'] < 1000:
                self.pixelData[i]["val"] += self.speed
                if self.pixelData[i]["val"] >= 1000:
                    if i+1 < self.numPixels:
                        self.pixelData[i+1]['active'] = True
                    else:
                        return False # Tells animator that the animation has ended
                    self.pixelData[i]["val"] = 1000

        rgbList = []
        for i in range(len(self.pixelData)):
            rgbList.append([self.color[0]*self.pixelData[i]['val']/1000,self.color[1]*self.pixelData[i]['val']/1000,self.color[2]*self.pixelData[i]['val']/1000])
        return rgbList
    
    def reset(self):
        for i in range(self.numPixels):
            self.pixelData[i] = {
                'val': 0,
                'active': False
            }

if __name__ == '__main__':
    print("This is a module, and is not meant to be used directly!")
    print("Animation output with following settings:")
    print("{'numPixels': 10, 'speed': 500}")
    print('\n')
    time.sleep(1)
    colorWipe = ColorWipe({'numPixels': 10, 'speed': 500})

    while True:
        colorData = colorWipe.animateFrame()
        print(colorData)
        if not colorData:
            break
        time.sleep(0.017)