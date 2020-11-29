from flask import Blueprint
from flask import request, jsonify

import client
from apiauth import require_apikey

thingsroute = Blueprint('things', __name__)

things = client.db.collection('things')

@thingsroute.route('/things', methods=['POST'])
@require_apikey
def creatething():

	try:
		id = request.json['id']
		things.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@thingsroute.route('/things', methods=['GET'])
@require_apikey
def readthing():

	try:
		all_things = [doc.to_dict() for doc in things.stream()]
		jsonresult = jsonify({"things" : all_things}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@thingsroute.route('/things/<id>', methods=['GET'])
@require_apikey
def readonething(id):

	try:
		thing = things.document(id).get()
		return jsonify(thing.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@thingsroute.route('/things/<id>', methods=['PUT'])
@require_apikey
def updatething(id):

	try:
		id = request.json['id']
		things.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@thingsroute.route('/things/<id>', methods=['DELETE'])
@require_apikey
def deletething(id):

	try:
		things.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

