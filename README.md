# Simple automatic Twitch stream recorder
Record Twitch streams live with streamlink. The stream is polled for being live. Output files are .ts MPEG-2
which is a convenient, if not very space-efficient, video format because you can append two .ts files to play
one after the other.

## Install
Install Python 3. Use pip to install streamlink with this command:

`pip install -r requirements.txt`

## Features
* Polls live status of the streamer every 5 seconds
* Can be left running indefinitely. After the stream ends, it starts polling again
* File name has the stream title
* If a stream title is not yet available, recording starts immediately and renames the video file later
* Streamer name can be passed in via command line
* Fancy spinner to stare at like a washing machine
* No need for API keys

## Usage
In your system's terminal, execute the script to record the default streamer:

`python twitch_recorder.py`

Depending on your system and install, the name of python may be python3 or python3.8, python3.9, etc.

To record a different streamer to the default, type their name after the script name:

`python twitch_recorder.py vargskelethor`

To change the default streamer, edit the string at the top of the script where it says `streamer = "..."`

To save the videos in a different directory, write a second argument to the script with the path:

`python twitch_recorder.py drdisrespect ../videos/`

The directory it points to must exist already. The script will not create the given directory and will error
if it doesn't exist.

The default file save location is also at the top of the script. It is "./" which is the current directory
of the terminal that launches python. 

## Issues
After the first stream has been recorded, it spams the console with errors from streamlink. 
