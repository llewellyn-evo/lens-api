#import for time options
import time
#import for threading options
import threading
#import to handle json
from flask_api import status 
import flask
from variables import app
import json
from smbus import SMBus
import os
import bme280

liquidLens = {}
data = None

bme_address = 0x76
bme280_calib = None

i2cbus = SMBus(1)  # Create a new I2C bus
i2cAddress = [0x23 , 0x77]

def save_values():
    global data
    try:
        filename = os.path.join(os.path.dirname(__file__), 'config/config.json')
        #Now we have the absolute path of the config file
	#Check if the file exists
        if os.path.isfile(filename):
            #If file found Load configs is module variable
            print("Saving Config to file.....")
            with open(filename, 'w') as outfile:
                json.dump(data , outfile)

    except Exception as e:
        print ("Exception Encountered " + str(e))



def getValues():
    try:
        print(i2cbus.read_byte_data(i2cAddress[1], 0x00))
        print(liquidLens)
        return 1
    except Exception as e:
        print("Error in getting i2c Values " + str(e))
        return -1

def setValues(val):
    global liquidLens
    try:
        if val[0] and val[0] < 256:
            i2cbus.write_byte(i2cAddress[0] , int(val[0]))
            liquidLens[0] = val[0]
            save_values()
        if val[1] and val[1] < 1024:
            i2cbus.write_byte_data(i2cAddress[1],0x04,int(val[1]) & 0x03 )
            i2cbus.write_byte_data(i2cAddress[1],0x05,int(val[1]) >> 2)
            i2cbus.write_byte_data(i2cAddress[1],0x09,0x02)
            liquidLens[1] = val[1]
            save_values()
        return 1
    except Exception as e:
        print("Write to i2c Failes " + str(e))

def setup_bme280():
    global bme280_calib
    try:
        bme280_calib = bme280.load_calibration_params(i2cbus, bme_address)
    except Exception as e:
        print("Error in getting bme280 calibration " + str(e))



def liquidLensProcess(module , exitEvent ):
    global liquidLens
    global data
    try:
        data = module
        liquidLens = module["liquid_lens"]
        #Set Up I2C device
        #SetUp 2nd i2C lens-controller ... Remote from Sleep Mode
        i2cbus.write_byte_data(i2cAddress[1],0x03,0x03)
        setValues(liquidLens)
        while not exitEvent.is_set():
            time.sleep(0.5)
    except Exception as e:
        print("i2C setup Failed" + str(e))

@app.route('/bme280' , methods = ["GET"])
def bme280data():
    global bme280_calib
    try:
        # compensated_reading object
        data = bme280.sample(i2cbus, bme_address, bme280_calib)
    
        return json.dumps({"temp": "{:.2f}".format(data.temperature), "hum": "{:.2f}".format(data.humidity), "pres" : "{:.2f}".format(data.pressure)}), status.HTTP_200_OK
    except Exception as e:
        print("Error in reading bme280 ", str(e))
        return "Error in reading bme280 device" ,status.HTTP_503_SERVICE_UNAVAILABLE


@app.route('/liquidLens' , methods = ["GET" , "POST"])
def xbeeConfigApi():
    if flask.request.method == "GET":
        resp = getValues()
        if resp == 1:
            return json.dumps({'values' : liquidLens }) , status.HTTP_200_OK
        elif resp == -1:
            return "Error in reading device" ,status.HTTP_503_SERVICE_UNAVAILABLE

    elif flask.request.method == "POST":
        content = flask.request.get_json()
        print (content)
        if "values" in content:
            setValues(content["values"])
        return "OK", status.HTTP_200_OK
