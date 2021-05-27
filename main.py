import time
from variables import *
#import to handle JSON objects and files
import json
import os

from flask_api import status 
import flask

from liquidlenshandler import liquidLensProcess


def read_config():
    config = default

    try:
        filename = os.path.join(os.path.dirname(__file__), 'config/config.json')
        #Now we have the absolute path of the config file
        #Check if the file exists
        print(filename)
        if os.path.isfile(filename):
            #If file found Load configs is module variable
            print("Config file exits .. Loading now !")
            with open(filename) as config_file:
                config = json.load(config_file)

    except Exception as e:
        print ("Exception Encountered " + str(e))

    #pretty print the loaded json config
    print (json.dumps(config, indent=4, sort_keys=True))

    return config




def main():

	global module
	#Read Configs
	module = read_config()

	liquidLensThread = threading.Thread(target = liquidLensProcess , args = ( module , exitEvent))
	liquidLensThread.start()

	app.run(host="0.0.0.0", port=8001)
	exitEvent.set()
	if liquidLensThread.is_alive():
		liquidLensThread.join()

	print("Exitting the Server Now .. ! ")



@app.route('/')
def hello_world():
	return 'Hello World'

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("DONE... Program Exiting...\n\n")
