import requests, eventlet
eventlet.monkey_patch()

serverAddress0 = 1
serverAddress1 = 0

while True:
    try:
        with eventlet.Timeout(0.1):
            res = requests.get(f"http://192.168.{serverAddress0}.{serverAddress1}:3000/ping").json()
            if res["serverName"] == "lightController":
                print("Address found")
                break
        if serverAddress1 > 255:
            serverAddress0 += 1
            serverAddress1 = 0
        else:
            serverAddress1 += 1
        print(serverAddress0, serverAddress1)
        
    except:
        if serverAddress1 > 255:
            serverAddress0 += 1
            serverAddress1 = 0
        else:
            serverAddress1 += 1
        print(serverAddress0, serverAddress1)
