from flask import Blueprint
from flask import request, jsonify
from firebase_admin import firestore

import client
from apiauth import require_apikey

yournewcollectionsroute = Blueprint('yournewcollections', __name__)

yournewcollections = client.db.collection('yournewcollections')

@yournewcollectionsroute.route('/yournewcollections', methods=['POST'])
@require_apikey
def create_yournewcollections():

	try:
		id = request.json['id']

		#server side timestamps from firestore, so now we don't need this calc in appsheet
		request.json['timestamp'] = firestore.SERVER_TIMESTAMP

		yournewcollections.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@yournewcollectionsroute.route('/yournewcollections', methods=['GET'])
@require_apikey
def read_yournewcollections():

	try:
		all_yournewcollections = [doc.to_dict() for doc in yournewcollections.order_by(u'timestamp').stream()]
		jsonresult = jsonify({"yournewcollections" : all_yournewcollections}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@yournewcollectionsroute.route('/yournewcollections/<id>', methods=['GET'])
@require_apikey
def readone_yournewcollections(id):

	try:
		_yournewcollection = yournewcollections.document(id).get()
		return jsonify(_yournewcollection.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@yournewcollectionsroute.route('/yournewcollections/<id>', methods=['PUT'])
@require_apikey
def update_yournewcollections(id):

	try:
		id = request.json['id']
		yournewcollections.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@yournewcollectionsroute.route('/yournewcollections/<id>', methods=['DELETE'])
@require_apikey
def delete_yournewcollections(id):

	try:
		yournewcollections.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

