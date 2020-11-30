import os
from datetime import datetime
from multiprocessing import Process
from flask import Flask, request, jsonify

import client as client
from heartbeat import heartbeat
from apiauth import require_apikey

from route_events import eventsroute
from route_persons import personsroute
from route_places import placesroute
from route_things import thingsroute
from route_contents import contentsroute
from route_settings import settingsroute
from route_init import initroute

app = Flask(__name__)
app.register_blueprint(eventsroute)
app.register_blueprint(personsroute)
app.register_blueprint(placesroute)
app.register_blueprint(thingsroute)
app.register_blueprint(contentsroute)
app.register_blueprint(settingsroute)
app.register_blueprint(initroute)

@app.route('/oaspec', methods=['GET'])
@require_apikey
def getoas():

	# we are opening and reading oas.yml on each request. This is because the 
	# /init route may update the target server URL value in this file
	try:
		oas = open('misc/oas.yml', 'r').read()	
		return oas
	except Exception as e:
		return f"An Error Occurred reading oas spec: {e}"
		
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':

	# comment the next two lines to disable our heartbeat event generator
	# otherwise, we are starting this on a seperate process
	heartbeat_process = Process(target=heartbeat)
	heartbeat_process.start()

	app.run(threaded=True, host='0.0.0.0', port=8080)



