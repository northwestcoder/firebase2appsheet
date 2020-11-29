from flask import Blueprint
from flask import request, jsonify

import client
from apiauth import require_apikey

contentsroute = Blueprint('contents', __name__)

contents = client.db.collection('contents')


@contentsroute.route('/contents', methods=['POST'])
@require_apikey

def createcontent():

	try:
		id = request.json['id']
		contents.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@contentsroute.route('/contents', methods=['GET'])
@require_apikey

@require_apikey

def readcontent():

	try:
		all_contents = [doc.to_dict() for doc in contents.stream()]
		jsonresult = jsonify({"contents" : all_contents}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@contentsroute.route('/contents/<id>', methods=['GET'])
@require_apikey

def readonecontent(id):

	try:
		content = contents.document(id).get()
		return jsonify(content.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@contentsroute.route('/contents/<id>', methods=['POST', 'PUT'])
@require_apikey

def updatecontent(id):

	try:
		id = request.json['id']
		contents.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@contentsroute.route('/contents/<id>', methods=['DELETE'])
@require_apikey

def deletecontent(id):

	try:
		contents.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

