import ws281xSC, datetime
LEDs = ws281xSC.LEDs(149, "http://192.168.1.124:3000")

def getTime():
    dt = datetime.datetime.today()
    dt.strftime("%M")
    return f"{dt.strftime('%w')}-{dt.strftime('%H')}-{dt.strftime('%M')}"

alarmTimes = ["4-15-05", "4-15-05", "4-15-08"]

print(alarmTimes)
print(getTime())

for alarmTime in alarmTimes:
    if getTime() == alarmTime:
        LEDs.setMode("alarmClockEC")