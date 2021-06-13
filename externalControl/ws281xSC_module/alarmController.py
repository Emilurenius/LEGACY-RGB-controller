import ws281xSC, datetime, time
LEDs = ws281xSC.strip(149, "http://192.168.1.124:3000")

def getTime():
    dt = datetime.datetime.today()
    dt.strftime("%M")
    return f"{dt.strftime('%w')}-{dt.strftime('%H')}-{dt.strftime('%M')}"

alarmTimes = LEDs.getJSON("alarmTimes.json")["times"]
print(alarmTimes)

while True:
    alarmTimes = LEDs.getJSON("alarmTimes.json")["times"]
    for alarmTime in alarmTimes:
        if getTime() == alarmTime:
            LEDs.setState(True)
            LEDs.setMode("alarmClockEC")
            time.sleep(61)