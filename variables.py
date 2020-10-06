import threading 
from flask import Flask
#import to fix CORS error
from flask_cors import CORS

module = {}


default = {
	'liquid_lens' : [ 50 , 50],
	'light'	: 50	
}

#Variables for Threading 
exitEvent= threading.Event()
liquidLensThread = threading.Thread()

#Variables for REST API Server
app = Flask(__name__)
CORS(app)