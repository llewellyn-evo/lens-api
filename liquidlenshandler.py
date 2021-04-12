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


liquidLens = {}

i2cbus = SMBus(1)  # Create a new I2C bus
i2cAddress = [0x23 , 0x77]

def getValues():
    try:
        #liquidLens[0] = i2cbus.read_byte(0x23)
        print(liquidLens)
        return 1
    except Exception as e:
        print("Error in getting i2c Values " + str(e))
        return -1

def setValues(val):
    global liquidLens
    print(val)
    try:
        if val[0] and val[0] < 256:
            i2cbus.write_byte(i2cAddress[0] , int(val[0]))
            liquidLens[0] = val[0]
        if val[1] and val[1] < 256:
            i2cbus.write_byte_data(i2cAddress[1] , 0x01 , int(val[1]))
            liquidLens[1] = val[1]
        return 1
    except Exception as e:
        print("Write to i2c Failes " + str(e))


def liquidLensProcess(module , exitEvent ):
    global liquidLens
    try:
        liquidLens = module["liquid_lens"]
        print(liquidLens)
        #Set Up I2C device
        #SetUp 2nd i2C lens-controller
        i2cbus.write_byte_data(i2cAddress[1],0x00,0x01)
        setValues(liquidLens)
        #print(i2cbus.write_byte(0x76,liquidLens))
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
        if "values" in content:
            setValues(content["values"])
        return "OK", status.HTTP_200_OK
