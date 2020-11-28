import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
import time
from datetime import datetime
import string
import random
from multiprocessing import Process

app = Flask(__name__)


# TODO: refactor and modularize all of this.... :( 


# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
persons = db.collection('persons')
events = db.collection('events')
places = db.collection('places')
things = db.collection('things')
settings = db.collection('settings')
contents = db.collection('contents')


# settings and event polling

def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    uniqueid = ''.join(random.choice(chars) for _ in range(size))
    return uniqueid

def heartbeat():

	heartbeatstatus = db.collection(u'settings').document(u'heartbeat')
	status = heartbeatstatus.get().to_dict()["value"]

	while True:
		if (status == "ON"):	
			print("status is ON, we are in heartbeat mode")

			recordid = id_generator()
			now = datetime.now()

			try:
				ping = {'id': recordid, 'Name': 'heartbeat event ' + recordid, 'personid': '', 'placeid': '', 
						'thingid': '','eventtype' : 'party', 'timestamp' : now, 
						'duration': 3, 'address': '3051 NE 86th St, Seattle WA 98115', 
						'latlong': '47.680989, -122.303969', 'photo':'', 'barcode': '', 'notes' : ''}
			
				events.document(recordid).set(ping)
				heartbeatstatus = db.collection(u'settings').document(u'heartbeat')
				status = heartbeatstatus.get().to_dict()["value"]
			except Exception as e:
				return f"An Error Occurred: {e}"
		else:
			print("status is OFF, heartbeat mode paused")	
			heartbeatstatus = db.collection(u'settings').document(u'heartbeat')
			status = heartbeatstatus.get().to_dict()["value"]
		time.sleep(60)


@app.route('/settings', methods=['GET'])
def readsettings():

	try:
		all_settings = [doc.to_dict() for doc in settings.stream()]
		jsonresult = jsonify({"settings" : all_settings}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@app.route('/settings/<id>', methods=['PUT'])
def updateheartbeat(id):

	try:
		id = request.json['id']
		settings.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


# ALL OTHER ROUTES



@app.route('/oaspec', methods=['GET'])
def getoas():
	try:
		oas = open('oas.yml', 'r').read()	
		return oas
	except Exception as e:
		return f"An Error Occurred reading oas spec: {e}"

@app.route('/persons', methods=['POST'])
def createperson():

	try:
		id = request.json['id']
		persons.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@app.route('/persons', methods=['GET'])
def readperson():

	try:
		all_persons = [doc.to_dict() for doc in persons.stream()]
		jsonresult = jsonify({"persons" : all_persons}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@app.route('/persons/<id>', methods=['GET'])
def readoneperson(id):

	try:
		person = persons.document(id).get()
		return jsonify(person.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/persons/<id>', methods=['POST', 'PUT'])
def updateperson(id):

	try:
		id = request.json['id']
		persons.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/persons/<id>', methods=['DELETE'])
def deleteperson(id):

	try:
		persons.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/events', methods=['POST'])
def createevent():

	try:
		id = request.json['id']
		events.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@app.route('/events', methods=['GET'])
def readevent():

	try:
		all_events = [doc.to_dict() for doc in events.stream()]
		jsonresult = jsonify({"events" : all_events}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@app.route('/events/<id>', methods=['GET'])
def readoneevent(id):

	try:
		event = events.document(id).get()
		return jsonify(event.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/events/<id>', methods=['POST', 'PUT'])
def updateevent(id):

	try:
		id = request.json['id']
		events.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/events/<id>', methods=['DELETE'])
def deleteevent(id):

	try:
		events.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"



@app.route('/places', methods=['POST'])
def createplace():

  try:
    id = request.json['id']
    places.document(id).set(request.json)
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"

@app.route('/places', methods=['GET'])
def readplace():

  try:
    all_places = [doc.to_dict() for doc in places.stream()]
    jsonresult = jsonify({"places" : all_places}), 200
    return jsonresult
  except Exception as e:
    return f"An Error Occurred: {e}"

@app.route('/places/<id>', methods=['GET'])
def readoneplace(id):

  try:
    place = places.document(id).get()
    return jsonify(place.to_dict()), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@app.route('/places/<id>', methods=['POST', 'PUT'])
def updateplace(id):

  try:
    id = request.json['id']
    places.document(id).update(request.json)
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@app.route('/places/<id>', methods=['DELETE'])
def deleteplace(id):

  try:
    places.document(id).delete()
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@app.route('/things', methods=['POST'])
def creatething():

	try:
		id = request.json['id']
		things.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@app.route('/things', methods=['GET'])
def readthing():

	try:
		all_things = [doc.to_dict() for doc in things.stream()]
		jsonresult = jsonify({"things" : all_things}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@app.route('/things/<id>', methods=['GET'])
def readonething(id):

	try:
		thing = things.document(id).get()
		return jsonify(thing.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/things/<id>', methods=['POST', 'PUT'])
def updatething(id):

	try:
		id = request.json['id']
		things.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/things/<id>', methods=['DELETE'])
def deletething(id):

	try:
		things.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@app.route('/contents', methods=['POST'])
def createcontent():

  try:
    id = request.json['id']
    contents.document(id).set(request.json)
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"

@app.route('/contents', methods=['GET'])
def readcontent():

  try:
    all_contents = [doc.to_dict() for doc in contents.stream()]
    jsonresult = jsonify({"contents" : all_contents}), 200
    return jsonresult
  except Exception as e:
    return f"An Error Occurred: {e}"

@app.route('/contents/<id>', methods=['GET'])
def readonecontent(id):

  try:
    content = contents.document(id).get()
    return jsonify(content.to_dict()), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@app.route('/contents/<id>', methods=['PUT'])
def updatecontent(id):

  try:
    id = request.json['id']
    contents.document(id).update(request.json)
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"


@app.route('/contents/<id>', methods=['DELETE'])
def deletecontent(id):

  try:
    contents.document(id).delete()
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occurred: {e}"
    
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
	heartbeat_process = Process(target=heartbeat)
	heartbeat_process.start()
	app.run(threaded=True, host='0.0.0.0', port=8080)



