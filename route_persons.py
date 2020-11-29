from flask import Blueprint
from flask import request, jsonify

import client

personsroute = Blueprint('persons', __name__)

persons = client.db.collection('persons')


@personsroute.route('/persons', methods=['POST'])
def createperson():

	try:
		id = request.json['id']
		persons.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@personsroute.route('/persons', methods=['GET'])
def readperson():

	try:
		all_persons = [doc.to_dict() for doc in persons.stream()]
		jsonresult = jsonify({"persons" : all_persons}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@personsroute.route('/persons/<id>', methods=['GET'])
def readoneperson(id):

	try:
		person = persons.document(id).get()
		return jsonify(person.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@personsroute.route('/persons/<id>', methods=['POST', 'PUT'])
def updateperson(id):

	try:
		id = request.json['id']
		persons.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@personsroute.route('/persons/<id>', methods=['DELETE'])
def deleteperson(id):

	try:
		persons.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

