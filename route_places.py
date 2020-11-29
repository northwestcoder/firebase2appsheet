from flask import Blueprint
from flask import request, jsonify

import client
from apiauth import require_apikey

placesroute = Blueprint('places', __name__)

places = client.db.collection('places')


@placesroute.route('/places', methods=['POST'])
@require_apikey

def createplace():

	try:
		id = request.json['id']
		places.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@placesroute.route('/places', methods=['GET'])
@require_apikey

def readplace():

	try:
		all_places = [doc.to_dict() for doc in places.stream()]
		jsonresult = jsonify({"places" : all_places}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@placesroute.route('/places/<id>', methods=['GET'])
@require_apikey

def readoneplace(id):

	try:
		place = places.document(id).get()
		return jsonify(place.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@placesroute.route('/places/<id>', methods=['POST', 'PUT'])
@require_apikey

def updateplace(id):

	try:
		id = request.json['id']
		places.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@placesroute.route('/places/<id>', methods=['DELETE'])
@require_apikey

def deleteplace(id):

	try:
		places.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

