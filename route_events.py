from flask import Blueprint
from flask import request, jsonify

import client
from apiauth import require_apikey

eventsroute = Blueprint('events', __name__)

events = client.db.collection('events')


@eventsroute.route('/events', methods=['POST'])
@require_apikey

def createevent():

	try:
		id = request.json['id']
		events.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@eventsroute.route('/events', methods=['GET'])
@require_apikey

def readevent():

	try:
		all_events = [doc.to_dict() for doc in events.stream()]
		jsonresult = jsonify({"events" : all_events}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@eventsroute.route('/events/<id>', methods=['GET'])
@require_apikey

def readoneevent(id):

	try:
		event = events.document(id).get()
		return jsonify(event.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@eventsroute.route('/events/<id>', methods=['POST', 'PUT'])
@require_apikey

def updateevent(id):

	try:
		id = request.json['id']
		events.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@eventsroute.route('/events/<id>', methods=['DELETE'])
@require_apikey

def deleteevent(id):

	try:
		events.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"
