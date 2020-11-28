import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

import oaspec

app = Flask(__name__)


# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
persons = db.collection('persons')
events = db.collection('events')
places = db.collection('places')
things = db.collection('things')

@app.route('/oaspec', methods=['GET'])
def getoas():
	try:
		oas = open('oas.yml', 'r').read()	
		return oas
	except Exception as e:
		return f"An Error Occured reading oas spec: {e}"

@app.route('/persons', methods=['POST'])
def createperson():

	try:
		id = request.json['id']
		persons.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"

@app.route('/persons', methods=['GET'])
def readperson():

	try:
		all_persons = [doc.to_dict() for doc in persons.stream()]
		jsonresult = jsonify({"persons" : all_persons}), 200
#		appsheetresult["persons"] = jsonresult
		return jsonresult
#		return jsonify("persons" : all_persons), 200
	except Exception as e:
		return f"An Error Occured: {e}"

@app.route('/persons/<id>', methods=['GET'])
def readoneperson(id):

	try:
		todo = persons.document(id).get()
		return jsonify(todo.to_dict()), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/persons/<id>', methods=['POST', 'PUT'])
def updateperson(id):

	try:
		id = request.json['id']
		persons.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/persons/<id>', methods=['DELETE'])
def deleteperson(id):

	try:
		persons.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/events', methods=['POST'])
def createevent():

	try:
		id = request.json['id']
		events.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"

@app.route('/events', methods=['GET'])
def readevent():

	try:
		all_events = [doc.to_dict() for doc in events.stream()]
		jsonresult = jsonify({"events" : all_events}), 200
#		appsheetresult["events"] = jsonresult
		return jsonresult
#		return jsonify("events" : all_events), 200
	except Exception as e:
		return f"An Error Occured: {e}"

@app.route('/events/<id>', methods=['GET'])
def readoneevent(id):

	try:
		todo = events.document(id).get()
		return jsonify(todo.to_dict()), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/events/<id>', methods=['POST', 'PUT'])
def updateevent(id):

	try:
		id = request.json['id']
		events.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/events/<id>', methods=['DELETE'])
def deleteevent(id):

	try:
		events.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"



@app.route('/places', methods=['POST'])
def createplace():

  try:
    id = request.json['id']
    places.document(id).set(request.json)
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occured: {e}"

@app.route('/places', methods=['GET'])
def readplace():

  try:
    all_places = [doc.to_dict() for doc in places.stream()]
    jsonresult = jsonify({"places" : all_places}), 200
#   appsheetresult["places"] = jsonresult
    return jsonresult
#   return jsonify("places" : all_places), 200
  except Exception as e:
    return f"An Error Occured: {e}"

@app.route('/places/<id>', methods=['GET'])
def readoneplace(id):

  try:
    todo = places.document(id).get()
    return jsonify(todo.to_dict()), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@app.route('/places/<id>', methods=['POST', 'PUT'])
def updateplace(id):

  try:
    id = request.json['id']
    places.document(id).update(request.json)
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@app.route('/places/<id>', methods=['DELETE'])
def deleteplace(id):

  try:
    places.document(id).delete()
    return jsonify({"success": True}), 200
  except Exception as e:
    return f"An Error Occured: {e}"


@app.route('/things', methods=['POST'])
def creatething():

	try:
		id = request.json['id']
		things.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"

@app.route('/things', methods=['GET'])
def readthing():

	try:
		all_things = [doc.to_dict() for doc in things.stream()]
		jsonresult = jsonify({"things" : all_things}), 200
#		appsheetresult["things"] = jsonresult
		return jsonresult
#		return jsonify("things" : all_things), 200
	except Exception as e:
		return f"An Error Occured: {e}"

@app.route('/things/<id>', methods=['GET'])
def readonething(id):

	try:
		todo = things.document(id).get()
		return jsonify(todo.to_dict()), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/things/<id>', methods=['POST', 'PUT'])
def updatething(id):

	try:
		id = request.json['id']
		things.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/things/<id>', methods=['DELETE'])
def deletething(id):

	try:
		things.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"


port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
	app.run(threaded=True, host='0.0.0.0', port=8080)

