#import for time options
import time
#import for threading options
import threading
#import to handle json
from flask_api import status 
import flask
from variables import app
import json

liquidLens = {}

def getValues():
	return 1



def liquidLensProcess(module , exitEvent ):
	global liquidLens
	try:
		liquidLens = module["liquid_lens"]
		print(liquidLens)
		#Set Up I2C device
		while not exitEvent.is_set():
			time.sleep(0.5)

	except Exception as e:
		print("i2C setup Failed" + str(e))


@app.route('/liquidLens' , methods = ["GET" , "POST"])
def xbeeConfigApi():
	if flask.request.method == "GET":
		resp = getValues()
		if resp == 1:
			return json.dumps({'values' : liquidLens }) , status.HTTP_200_OK
		elif resp == -1:
			return "Error in reading device" ,status.HTTP_503_SERVICE_UNAVAILABLE

	elif flask.request.method == "POST":
		print("Set Values Here")
		print (flask.request.is_json)
		content = flask.request.get_json()
		print (content)
		return "OK", status.HTTP_200_OK