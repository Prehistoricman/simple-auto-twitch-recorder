# Simple automatic Twitch stream recorder
Record Twitch streams live with streamlink. The stream is polled for being live. Output files are .ts MPEG-2 which is a convenient, if not very space-efficient, video format because you can append two .ts files to play one after the other.

## Install
Install Python 3. Use pip to install streamlink with this command:

`pip install -r requirements.txt`

## Features
* Polls live status of the streamer every 5 seconds
* Can be left running indefinitely. After the stream ends, it starts polling again
* File name has the stream title
* If a stream title is not yet available, recording starts immediately and renames the video file later
* Streamer name can be passed in via command line
* No need for API keys

## Issues
After the first stream has been recorded, it spams the console with errors from streamlink. 
