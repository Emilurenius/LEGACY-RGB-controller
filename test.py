import time

def timePrint(printVal):
    currentTime = time.strftime("%H:%M:%S", time.localtime())
    print(f"{currentTime}: {printVal}")

timePrint("Hello world")