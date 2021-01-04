import RPi.GPIO as GPIO
from datetime import datetime, timedelta
import pickle

pin = 11
buttons = []

#Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

#Gets binary value
def getBinary():
	#Internal vars
	num1s = 0 #Number of consecutive 1s read
	binary = 1 #The bianry value
	command = [] #The list to store pulse times in
	previousValue = 0 #The last value
	value = GPIO.input(pin) #The current value
	
	#Waits for the sensor to pull pin low
	while value:
		value = GPIO.input(pin)
		
	#Records start time
	startTime = datetime.now()
	
	while True:
		#If change detected in value
		if previousValue != value:
			now = datetime.now()
			pulseTime = now - startTime #Calculate the time of pulse
			startTime = now #Reset start time
			command.append((previousValue, pulseTime.microseconds)) #Store recorded data
			
		#Updates consecutive 1s variable
		if value:
			num1s += 1
		else:
			num1s = 0
		
		#Breaks program when the amount of 1s surpasses 10000
		if num1s > 10000:
			break
			
		#Re-reads pin
		previousValue = value
		value = GPIO.input(pin)
		
	#Converts times to binary
	for (typ, tme) in command:
		if typ == 1: #If looking at rest period
			if tme > 1000: #If pulse greater than 1000us
				binary = binary *10 +1 #Must be 1
			else:
				binary *= 10 #Must be 0
			
	if len(str(binary)) > 34: #Sometimes, there is some stray characters
		binary = int(str(binary)[:34])
		
	return binary
	
#Conver value to hex
def convertHex(binaryValue):
	tmpB2 = int(str(binaryValue),2) #Tempary propper base 2
	return hex(tmpB2)

previousVal = False
mode = input(">>")
print(mode)

if mode == "test":
	while True:
		inData = convertHex(getBinary())
		print(inData)
		
		if previousVal:
			if previousVal == inData:
				print("Same one again")
				previousVal = inData
			else:
				print("New button!")
				previousVal = inData
		else:
			print("Fist buttonpress")
			previousVal = inData

elif mode == "noiseReduce":
	noiseList = []
	noiseFoundTime = datetime.now().timestamp()
	while datetime.now().timestamp() - noiseFoundTime < 20:
		noise = convertHex(getBinary())
		print(noise)

		if noise in noiseList:
			noiseFound = False
		else:
			noiseFound = True
			print("New noise signal found")
			noiseList.append(noise)

		if noiseFound:
			noiseFoundTime = datetime.now().timestamp()
		else:
			now = datetime.now()
			#This print statement does not do it's job
			#print("checking for", datetime.now().timestamp() - noiseFoundTime * -1, "more seconds")

	print("No more noise found!")
	print("noise found:", noiseList)
	open_file = open("noise.pkl", "wb")
	pickle.dump(noiseList, open_file)
	open_file.close()