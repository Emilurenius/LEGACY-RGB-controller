**NOTE**: This is not complete
# What will this page contain?
This page will be explaining how to connect to the web server controlling the script called lightController.py.

This page will show all available API calls, and what queries can be given. The response from the server will also be documented here.
More more specific examples of how to implement every API call, refer to this page: `link coming soon`

# Available API calls:

## /lightState:
### Available queries:
* toggle
  * Desc: Makes the server toggle lights if it equals "change"
  * Example: `http://serverAddress.com/lightState?toggle=change`
### Server response:
* Type: boolean
* desc: Gives the current state of the lights. true if lights are on, false if they are off. Note: If you change the value, it will send the value it changed to

## /checkLightState:
**DEPRECATED, use lightState instead**
### Available queries:
**None**
### Server response:
* Type: boolean
* desc: Represents the current state of the lights. true if the lights are on, false if they are not.

## /br:
### Available queries:
**None**
### Server response:
* Type: string
* desc: returns the current brightness as a string. The string will represent number between 0 and 1000. Divide by 1000 to get percentage.

## /r:
### Available queries:
**None**
### Server response:
* Type: string
* desc: Returns the current value for the red color channel as a string. The string will represent a number between 0 and 255

## /g:
### Available queries:
**None**
### Server response:
* Type: string
* desc: Returns the current value for the green color channel as a string. The string will represent a number between 0 and 255

## /b:
### Available queries:
**None**
### Server response:
* Type: string
* desc: Returns the current value for the blue color channel as a string. The string will represent a number between 0 and 255

## /rgb:
### Available queries:
* br: (integer between 0 and 1000)
  * Desc: Sets brightness of the lights to given value
  * Example: `http://serverAddress.com/rgb?br=1000`
  * **WARNING**: Giving this query a value over or under max value might lead to unforseen effects. There is currently no clamping serverside.
* r: (integer between 0 and 255)
  * Desc: Sets the red channel of the lights to given value
  * Example: `http://serverAddress.com/rgb?r=255`
  * **WARNING**: Giving this query a value over or under max value might lead to unforseen effects. There is currently no clamping serverside.
* g: (integer between 0 and 255)
  * Desc: Sets the green channel of the lights to given value
  * Example: `http://serverAddress.com/rgb?g=255`
  * **WARNING**: Giving this query a value over or under max value might lead to unforseen effects. There is currently no clamping serverside.
* b: (integer between 0 and 255)
  * Desc: Sets the blue channel of the lights to given value
  * Example: `http://serverAddress.com/rgb?b=255`
  * **WARNING**: Giving this query a value over or under max value might lead to unforseen effects. There is currently no clamping serverside.
### Server response:
* Type: String
* Desc: Will send one of two strings: `data recieved` or `no data recieved` based on whether or not any data has been saved serverside.

## /modes/set:
### Available queries:
* mode: (string)
  * Desc: Accepts all values, and sends them on to lightController.py serverside
  * Example: `http://serverAddress.com/modes/set?mode=standard`
  * **WARNING**: If the name of the mode you give is not defined on the server, the RGB lights will do nothing until a valid mode is given.
* elitusMode (string)
  * Desc: Works just like the query above, but this one is used to control how the elite dangerous (elitus) mode on the serverside acts.
  * Example: `http://serverAddress.com/modes/set?elitusMode=standard`
  * **WARNING**: This functionality is under testing, and has had very little development! Use at your own risk!
### Server response:
* Type: string
* Desc: Will send one of two strings: `data recieved: "currentMode"` or `no data recieved`. 
	"currentMode" will be the mode you just changed it to. This can be used to double check if the server got the right value during testing.

## /modes/current:
### Available queries:
**None**
### Server response:
* Type: string
* Desc: returns the name of the current mode

## /colorPresets
### Available queries:
* mode: (string)
  * accepted values: ("new", "load")
  * Desc: based on what mode you ask for, you can either load already created color presets, or create a new one.
  * Example: `http://serverAddress.com/colorPresets?mode=new`
* r: (integer between 0 and 255)
  * Desc: If the query "mode" is set to "new", the value of this query will be used as the red channel for the new color preset
  * Example: `http://serverAddress.com/colorPresets?r=255`
* g: (integer between 0 and 255)
  * Desc: If the query "mode" is set to "new", the value of this query will be used as the green channel for the new color preset
  * Example: `http://serverAddress.com/colorPresets?g=255`
* b: (integer between 0 and 255)
  * Desc: If the query "mode" is set to "new", the value of this query will be used as the blue channel for the new color preset
  * Example: `http://serverAddress.com/colorPresets?b=255`
* presetName: (string)
  * Desc: If the query "mode" is set to "new" the value of this query will be used as the name of the new color preset
  * Example: `http://serverAddress.com/colorPresets?presetName=myPreset`
### Server response:
* If the query "mode" is set to "new":
  * Type: String
  * Desc: If all went well on the server side, the response will always be: `"success"`
* If the query "mode" is set to "load":
* Type: JSON
  * Desc: This JSON file includes all previously defined presets structured like this: 

  ```
  {
	  "red": {
      "r": 255,
      "g": 0,
      "b": 0
      }
  }
  ```

## /bpm:
### Available queries:
* Mode: (string)
  * Accepted values: (updateBPM, spotifySync, spotifyResponse) **NOTE**: spotifyResponse is a value that should only be given with a response from spotify.
  * Desc: This query decides what the API call will do with the information given. updateBPM takes one extra query: "bpm"
  * Example: `http://serverAddress.com/bpm?mode=updateBPM&bpm=50`
* bpm: (float)
  * Desc: This query is used by the modes "updateBPM" and "spotifyResponse". The way this query is processed does not change between these modes. In the mode "spotifySync", this query will be ignored by the API.
  * Example: `http://serverAddress.com/bpm?mode=updateBPM&&bpm=50` or `http://serverAddress.com/bpm?mode=spotifyResponse&bpm=50&messageSent=`
  * **WARNING**: If the mode spotifyResponse is used, and only the bpm query is given, this will cause an error on the API server, please check the other queries available for this API call before using it!
* messageSent: (timestamp represented as integer)
	* Desc: This query is used by the server to properly syncromize with spotify. This value should only be assigned the current time when the request is sent as a timestamp in milliseconds.
	By giving the server this value, you are assured that the server knows when you did the calculations on your end, and will correct for any and all
	delay between you and the server.
	* Example: `http://serverAddress.com/bpm?mode=spotifyResponse&bpm=50&messageSent=1617786197749&currentSongProgress=50`
	* **WARNING**: Giving this query an outdated timestamp, or a timestamp set in the future will make the script either constantly look for the next song,
	or just freeze untill the future timestamp closes in.
* currentSongProgress:
	* Desc: This query represents the amount of milliseconds since the song started playing. This value is given by the spotify API, and is used to sync the BPM of the lights with the beat in the currently playing song.
	* Example: `http://serverAddress.com/bpm?mode=spotifyResponse&bpm=50&messageSent=1617786197749&currentSongProgress=50`
### Server response:
* If the query "mode" is set to "updateBPM":
	* Type: string
	* Desc: The string response from the server will always be `"success"` if the API could complete the request
* If the query "mode" is set to "spotifySync":
	* Type: redirect
	* Desc: This mode is used for connecting to the spotify API, and can be bypassed if you have your own way of talking to the spotify API.
	Just be aware that connecting through this way requires some tweaking on your end. For more info on that, search up how to connect to the spotify API.
	* **WARNING** This mode, and the response from it is currently set up to work for my setup. You might want another approach.
* If the query "mode" is set to "spotifyResponse":
	* Type: string representing a number
	* Desc: The response will be the bpm of the currently playing song that the lights now has synced to.
	This could be used to update a website's UI with the current bpm, like the website included with the server.'

## /settings/standard:
### Available queries:
* colorChange: (string)
	* Accepted values: (fade, wipe)
	* Desc: This query changes the behaviour of standard mode for the lights.
		If given the value "fade", the lights will nicely fade between the old color, and the new one given.
		If given the value "wipe", the lights will wipe the new color over the old one.
	* Example: `http://serverAddress.com/settings/standard?colorChange=fade`
### Server response:
* Type: JSON
* Desc: The server will send the standard settings file located on the server as a response.
	If values were changed with one of the queries above, this will be updated before the file is sent.
	This means that the values inside the JSON file are always up to date with the settings for standard mode.
* Example:

		```
		{
    	"colorChange": "wipe"
		}
		```