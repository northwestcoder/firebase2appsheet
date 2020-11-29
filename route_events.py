from flask import Blueprint
from flask import request, jsonify
from firebase_admin import firestore

import client
from apiauth import require_apikey

eventsroute = Blueprint('events', __name__)

events = client.db.collection('events')

@eventsroute.route('/events', methods=['POST'])
@require_apikey
def createevent():

	try:
		id = request.json['id']

		#server side timestamps from firestore, now we don't need this calc in appsheet
		request.json['timestamp'] = firestore.SERVER_TIMESTAMP

		events.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@eventsroute.route('/events', methods=['GET'])
@require_apikey
def readevent():

	try:
		all_events = [doc.to_dict() for doc in events.order_by(u'timestamp').stream()]
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


@eventsroute.route('/events/<id>', methods=['PUT'])
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

