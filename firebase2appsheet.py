import os
from datetime import datetime
from multiprocessing import Process
from flask import Flask, request, jsonify
import logging as log

import client as client
from heartbeat import heartbeat
from apiauth import require_apikey

from route_events import eventsroute
from route_persons import personsroute
from route_places import placesroute
from route_things import thingsroute
from route_contents import contentsroute
from route_settings import settingsroute

app = Flask(__name__)
app.register_blueprint(eventsroute)
app.register_blueprint(personsroute)
app.register_blueprint(placesroute)
app.register_blueprint(thingsroute)
app.register_blueprint(contentsroute)
app.register_blueprint(settingsroute)

import initialize as init


def getoas():
	try:
		oas = open('misc/oas.yml', 'r').read()	
		return oas
	except Exception as e:
		return f"An Error Occurred reading oas spec: {e}"

OASFILE = getoas()


@app.route('/oaspec', methods=['GET'])
@require_apikey
def getoas():

	return OASFILE
		
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':

	# comment the next two lines to disable our heartbeat event generator
	# otherwise, we are starting this on a seperate process
	heartbeat_process = Process(target=heartbeat)
	heartbeat_process.start()

	# comment out the next line if you don't want this demo creating a single
	# record per firestore collection
	runfirsttime = init.initialize()

	log.info(f"Some log here") 
	app.run(threaded=True, host='0.0.0.0', port=8080)



