from flask import Blueprint
from flask import request, jsonify

import client

settingsroute = Blueprint('things', __name__)

settings = client.db.collection('things')

@settingsroute.route('/settings', methods=['GET'])
def readsettings():

	try:
		all_settings = [doc.to_dict() for doc in settings.stream()]
		jsonresult = jsonify({"settings" : all_settings}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@settingsroute.route('/settings/<id>', methods=['PUT'])
def updateheartbeat(id):

	try:
		id = request.json['id']
		settings.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

