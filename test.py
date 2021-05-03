import requests, json

data = requests.get("http://192.168.1.124:3000/json/data.json").json()