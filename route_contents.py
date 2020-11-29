from flask import Blueprint
from flask import request, jsonify

import client

contentsroute = Blueprint('contents', __name__)

contents = client.db.collection('contents')


@contentsroute.route('/contents', methods=['POST'])
def createcontent():

	try:
		id = request.json['id']
		contents.document(id).set(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

@contentsroute.route('/contents', methods=['GET'])
def readcontent():

	try:
		all_contents = [doc.to_dict() for doc in contents.stream()]
		jsonresult = jsonify({"contents" : all_contents}), 200
		return jsonresult
	except Exception as e:
		return f"An Error Occurred: {e}"

@contentsroute.route('/contents/<id>', methods=['GET'])
def readonecontent(id):

	try:
		content = contents.document(id).get()
		return jsonify(content.to_dict()), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@contentsroute.route('/contents/<id>', methods=['POST', 'PUT'])
def updatecontent(id):

	try:
		id = request.json['id']
		contents.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"


@contentsroute.route('/contents/<id>', methods=['DELETE'])
def deletecontent(id):

	try:
		contents.document(id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occurred: {e}"

