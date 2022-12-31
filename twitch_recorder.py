import time
import sys
import os
import streamlink
session = streamlink.Streamlink()

streamer = "paymoneywubby" #Default streamer
files_directory = "./" #Default videos location

if len(sys.argv) >= 2: #Take command line argument for streamer name
    streamer = sys.argv[1]
if len(sys.argv) >= 3: #Take command line argument for file location
    files_directory = sys.argv[2]
    #Make sure the path ends in a slash
    if files_directory[-1] != "/" and files_directory[-1] != "\\":
        files_directory += "/"

session.set_plugin_option("twitch", "disable_hosting", 1) #Don't record a host or raid
session.set_option("stream-timeout", 30)
session.set_option("stream-segment-threads", 3)
session.set_option("ringbuffer-size", 16 * 1024 * 1024)

spins = ["|", "/", "-", "\\"]
spindex = 0
def print_spinner():
    global spindex
    print("\r" + spins[spindex], end="        ")
    spindex += 1
    if spindex == len(spins):
        spindex = 0

while True:
    try:
        streams = []
        print("Waiting for streamer " + streamer + " live...")
        streamurl = "https://twitch.tv/" + streamer
        while len(streams) == 0:
            streams = session.streams(streamurl) #Will return empty list if the stream is not live
            if len(streams) == 0:
                time.sleep(5)
            print_spinner()
        print()

        print(streams.keys())

        #List of quality settings to try
        try_keys = ["best", "1080p60", "1080p", "720p60", "720p"]
        stream = 0
        for i in range(len(try_keys)):
            if try_keys[i] in streams.keys():
                stream = streams[try_keys[i]]
                print("Using quality " + try_keys[i])
                break
        
        starttime = time.time()
        def getStreamTitle():
            try:
                pluginclass, resolved_url = session.resolve_url(streamurl)
                plugin = pluginclass(resolved_url)
                plugin.get_metadata()
                print("id: " + str(plugin.id))
                print("author: " + str(plugin.author))
                print("category: " + str(plugin.category))
                print("title: " + str(plugin.title))
                return str(plugin.title)

            except streamlink.NoPluginError:
                print(f"No plugin can handle URL: {streamurl}")
                return "None"
            except streamlink.PluginError as err:
                print(err)
                return "None"

        stream_title = getStreamTitle()

        def getOutputFilePath(start_time_str):
            filepath = "%s_%s_%s.ts" % (streamer, stream_title, start_time_str)
            #Filter out invalid chars from the file name
            filepath = "".join(c for c in filepath if c not in "\/:*?<>|")
            #Prepend the directory path
            filepath = files_directory + filepath
            return filepath

        start_time_str = time.strftime("%Y-%m-%d_%H-%M")
        output_filepath = getOutputFilePath(start_time_str)
        print("output file name " + output_filepath)

        total_bytes = 0
        rename = False
        print()
        try:
            stream_file = stream.open()
            
            firstrun = True #Hack to make a do-while loop
            while rename or firstrun:
                firstrun = False
                if rename:
                    rename = False
                    #Change name from output_filepath to the new output file path generated
                    new_filepath = getOutputFilePath(start_time_str)
                    print("Switching file name to " + new_filepath)
                    try:
                        os.rename(output_filepath, new_filepath)
                        output_filepath = new_filepath #Only execute this line if the rename works
                    except OSError:
                        pass
            
                with open(output_filepath, "ab") as out_file: # open for [a]ppending as [b]inary

                    while True:
                        data = stream_file.read(1024)

                        # If data is empty the stream has ended
                        if not data:
                            stream_file.close()
                            out_file.close()
                            break

                        total_bytes += len(data)
                        out_file.write(data)
                        print("\rMegabytes: %0.2f" % (total_bytes / 1000000), end="         ")
                        
                        if stream_title == "None" and not firstrun:
                            #See if we can get an updated title
                            newtitle = getStreamTitle()
                            if newtitle != "None":
                                rename = True
                                stream_title = newtitle
                                break
                    
        except streamlink.StreamError as err:
            print('StreamError: {0}'.format(err))

        print()
    except FileNotFoundError as e: #Occurs when the file path doesn't exist
        print(e)
        exit()
    except KeyboardInterrupt:
        exit()
    except Exception:
        pass