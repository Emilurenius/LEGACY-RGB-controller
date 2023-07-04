from animations.colorBubbles import ColorBubbles

class Animator:

    def __init__(self, numPixels, frameRate=60):

        self.numPixels = numPixels
        self.frameRate = frameRate
        self.delay_seconds = 1/self.frameRate # 1 split by frames per second

        self.animations = {
            'colorBubbles': ColorBubbles({'numPixels': numPixels})
        }

    def color(self, animation):
        return False
    
    def brightnessMask(self, animation):
        return False
    
    def shaderMask(self, animation):
        return False
    
    def process(self, animation):
        return False