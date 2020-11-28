import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app


import oaspec


# Initialize Flask App
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
persons = db.collection('persons')
events = db.collection('events')


@app.route('/oaspec', methods=['GET'])
def getoas():
	try:
	   return oaspec.oas_endpoint()
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




port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
	app.run(threaded=True, host='0.0.0.0', port=8080)


