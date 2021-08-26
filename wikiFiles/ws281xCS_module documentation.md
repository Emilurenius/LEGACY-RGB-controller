**NOTE**: This is not complete
# What will this page contain?
This page will explain how to use the ws281xSC_module in your own python scripts.

# Setup:

## How to access:
The module is currently not part of the pip ecosystem, so you will have to extract it from this repository.

the module can be found under  `/externalControl/ws281xSC_module/`. Name of the file is `ws281xSC.py`

You can either begin programming inside this directory, or copy the python module to your own directory.
The script should work regardless of where it is, as long as the script accessing it is in the same directory as the module.

## Quick start:

The library is imported like any other library or module with help of the `import` keyword

Here is an example of a script setting the server state to `true` and setting mode to `standard`, essentially turning the lights on:

```
import ws281xSC

strip = ws281xSC.strip(149, "http://192.168.1.124:3000") # Address will be different for you
strip.setMode("directRGB")

strip.setMode("standard")
strip.setState(True)
```

# strip class initialization:
The module consists of only one class containing everything you need to control the LED lights.

## How to initialize:
Initializing the strip class is done by giving it two variables: number of LEDs and the server address you want to control.

## Initialization variables:
* LEDcount: A number between 1 and infinity. Defines how many LEDs you wish to control on the defined server address.
* address: The address that points to the web server you want to send requests. Will look something like this: `http://192.168.1.124:3000`

# Available functions in strip class:

## checkAddress:
* variables: none
* response type: string
* example use: `address = checkAddress()`
* example response: `http://192.168.1.124:3000`

## printLEDdata
* variables: none
* response type: prints data in terminal
* example use: `printLEDdata()`
* example response: all LED data is printed in terminal

## percentofLEDs:
* variables:
    * percentage: int between 0 and 100
* response type: int (number of LEDs corresponding to percentage given)
* example use: `redLEDs = percentofLEDs(50)` (will give back a number equaling half of the LEDs on the strip)
* example response: `50`
