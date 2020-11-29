import os
from datetime import datetime
from multiprocessing import Process
from flask import Flask, request, jsonify

import client as client
from initializer import initialdata
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

@app.route('/oaspec', methods=['GET'])
def getoas():
	try:
		oas = open('oas.yml', 'r').read()	
		return oas
	except Exception as e:
		return f"An Error Occurred reading oas spec: {e}"
		
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
	heartbeat_process = Process(target=heartbeat)
	heartbeat_process.start()
	initialdata_process = Process(target=initialdata)
	initialdata_process.start()
	app.run(threaded=True, host='0.0.0.0', port=8080)



