import json, time, os

def breathe():
	br = 0
	try:
		
		with open("./json/data.json") as JSON:
			data = json.load(JSON)
			
	except:
		print("JSON busy...")
		time.sleep(0.05)
	
	while br < 256 and data["onoff"]:
		try:
		
			with open("./json/data.json") as JSON:
				data = json.load(JSON)
			
		except:
			print("JSON busy...")
			time.sleep(0.05)
		if data["mode"] != "breathe":
			break
		br += float(data["breatheSpeed"]) / 100
		print("Lightstate:", data["onoff"], "Mode:", data["mode"], "BR:", br, "R:", data["R"], "G:", data["G"], "B:", data["B"])
		time.sleep(0.01)
		
	while br > 0 and data["onoff"]:
		try:
		
			with open("./json/data.json") as JSON:
				data = json.load(JSON)
			
		except:
			print("JSON busy...")
			time.sleep(0.05)
		if data["mode"] != "breathe":
			break
		br -= float(data["breatheSpeed"]) / 100
		print("Lightstate:", data["onoff"], "Mode:", data["mode"], "BR:", br, "R:", data["R"], "G:", data["G"], "B:", data["B"])
		time.sleep(0.01)

while True:
	try:
		
		with open("./json/data.json") as JSON:
			data = json.load(JSON)
			
	except:
		print("JSON busy...")
		time.sleep(0.05)
		
	if data["onoff"] == False:
		data["brightness"] = 0
		print("Lightstate:", data["onoff"], "Mode:", data["mode"], "BR:", data["brightness"], "R:", data["R"], "G:", data["G"], "B:", data["B"])
		time.sleep(0.05)
		
	elif data["mode"] == "breathe":
			breathe()
			
	else:
		print("Lightstate:", data["onoff"], "Mode:", data["mode"], "BR:", data["brightness"], "R:", data["R"], "G:", data["G"], "B:", data["B"])
		time.sleep(0.05)
