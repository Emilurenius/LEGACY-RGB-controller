import ws281xSC, datetime, time
strip = ws281xSC.strip(149, "http://192.168.1.124:3000")

daysLookup = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

def getDay():
    dt = datetime.datetime.today()
    return dt.strftime('%w')

def getHour():
    dt = datetime.datetime.today()
    return dt.strftime('%H')

def getMin():
    dt = datetime.datetime.today()
    return dt.strftime('%M')

while True:
    time.sleep(1)
    alarmTimes = strip.getJSON("alarmTimes.json")

    for k,v in  alarmTimes.items():
        activeToday = v["days"][daysLookup[int(getDay())]] == "true"
        currentTime = v["time"] == f"{getHour()}:{getMin()}"
        if activeToday and currentTime:
            strip.setMode("alarmClockEC")
            strip.setState(True)
            print("Alarm activated")
            time.sleep(60)