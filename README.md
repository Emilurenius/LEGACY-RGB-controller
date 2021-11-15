# RGB-controller
A controller for WS2812b RGB strip on raspberry pi

# Setup:
For setting up your lights, follow this tutorial:
https://www.youtube.com/watch?v=Pxt9sGTsvFk

If you already know how to set up the lights, here's a reminder of a neat command that downloads everything:
`curl -L http://coreelec.io/33 | bash`

Now for my part of the script:

When You got everything set up, and strandtest runs fine, you will need to download the newest version of node on your raspberry pi:

with terminal:

`sudo apt install nodejs`
`sudo apt install npm`
`sudo apt update`

Or open this in a browser on the Pi:

https://nodejs.org/dist/v14.15.1/node-v14.15.1-linux-arm64.tar.xz


Then when node.js is up and running on your computer, you are ready to install the github repository.
Use your desired way to download the repository, and then open the directory called RGBserver. 
In here there are some files you have to run, and some files you can use if you want:

* app.js: Webserver for graphical interface (Needed)
* lightController.py: The script that acutally talks to the lights (Needed)
* ButtonController.py: A button controller I made for my own makeshift button. (Optional)
* clapSensor.py: A script taking information from a sound sensor that measured DB. Connected with the digital output. Sends 3.3 volts when DB over certain threshold. (optional)

To start the server, make sure you are in the RGBserver directory, and write this in the terminal: node app.js 3000

The number at the end is the port you want the server to run on. If you want another port, simply change this number.
Make sure the server is running by trying to open the website. To open the website, you need to know the IP address of your Pi. You can check that by writing this in the terminal:

hostname -I

The first number is your ipv4 address on your localhost. It should look like this: 192.168.1.124

Your numbers are most likely different

Now that you have the ipv4 address, check that the server is live by writing this in the address bar on any browser with any device on the same internet: 

http://192.168.1.124:3000

Remember to put in your own ip and port if they are different.

Now for lightController.py: This file shouldn't need any setup, so just open another terminal, and navigate to the same directory. Then write this in the terminal:

sudo python3 lightController.py

Using sudo is very important, since the script needs some access that linux won't give it otherwise in order to interface with the lights.

To start the other python scripts I listed above, simply use the same method as for lightController.py.
I will warn you though, those scripts are very experimental, and large changes may occur to them in future updates.
I would suggest you use them as inspiration for your own scripts, as they are made specifically for the hardware I have set up.

# Reasons things might not work:

## LightController.py not running:

Have you installed the library used by the script? If not, that might be the issue.

Needed library can be found here: https://github.com/jgarff/rpi_ws281x

If you are not sure if you have downloaded the library, check if the following directory exists: /home/pi/rpi_ws281x

If it's not there, navigate to "/home/pi" in the terminal on your raspberry pi (This is the directory that the terminal opens in) and write the following: git clone https://github.com/jgarff/rpi_ws281x

Now try again. If the script still won't run, create an issue in this repository, and I will do what I can to help you.

# Server Addresses and what they do:

index page: This is the main page of the website, and where you will get the control panel for the LED strip.

## /br: 

API page that returns the brightness level currently in use

## /r: 

API page that returns the red value currently in use

## /g: 

API page that returns the green value currently in use

## /b: 

API page that returns the green value currently in use

## /rgb: 

API page that allows control of brightness and RGB values of the server, and hence the lights.

## /mdoes/set: 

API page that allows control of what mode the lights are in.

# How to use the server API with python script running on the raspberry Pi:

## /br, /r, /g, /b: 

To talk to these addresses, you can use the module called "requests" https://pypi.org/project/requests/

write the following code to send a get request: response = requests.get("http://localhost:3000/br")

Then write this to print out the value returned: print(response.text)

# /rgb: 

This address can be used to control the brightness and color of the LED ligts. Here are the different queries you can use to control it:

* br: Control brightness in a range from 0 to 100. Values under or over the range may cause a crash for lightController.py
* r: Control the red channel of the LED lights in a range of 0 to 255. Values under or over the range may cause a crash for lightController.py
* g: Control the green channel of the LED lights in a range of 0 to 255. Values under or over the range may cause a crash for lightController.py
* b: Control the blue channel of the LED lights in a range of 0 to 255. Values under or over the range may cause a crash for lightController.py

This is how you can interface with the API through the requests module for python:

response = requests.get("http://localhost:3000/rgb?br=255&r=255&g=255&b=255")

print(response.text)

This will change the lights to white with maximum brightness, and print the response from the API

## /modes/set:

This address can be used to select a mode that is defined in lightController.py

If you set the mode to one that is not defined, this will not crash the server, or the script.

This is the way you can interface with the API through the requests module in python:

response = requests.get("http://localhost:3000/modes/set?mode=standard")

print(response.text)

This will change the mode to standard, and print the response from the API

