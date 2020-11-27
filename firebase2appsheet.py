# main entry point
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
def read():
	"""
		read() : Fetches documents from Firestore collection as JSON
		todo : Return document that matches query ID
		all_todos : Return all documents
	"""
	try:
		# Check if ID was passed to URL query
		todo_id = request.args.get('id')    
		if todo_id:
			todo = persons.document(todo_id).get()
			return jsonify(todo.to_dict()), 200
		else:
			all_todos = [doc.to_dict() for doc in persons.stream()]
			return jsonify(all_todos), 200
	except Exception as e:
		return f"An Error Occured: {e}"

@app.route('/persons/<id>', methods=['GET'])
def readone(id):

	try:
		todo = persons.document(id).get()
		return jsonify(todo.to_dict()), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/persons/{id}', methods=['POST', 'PUT'])
def update():
	"""
		update() : Update document in Firestore collection with request body
		Ensure you pass a custom ID as part of json body in post request
		e.g. json={'id': '1', 'title': 'Write a blog post today'}
	"""
	try:
		id = request.json['id']
		persons.document(id).update(request.json)
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"


@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
	"""
		delete() : Delete a document from Firestore collection
	"""
	try:
		# Check for ID in URL query
		todo_id = request.args.get('id')
		persons.document(todo_id).delete()
		return jsonify({"success": True}), 200
	except Exception as e:
		return f"An Error Occured: {e}"



#def appsheet2firebase():
#	test = oaspec.oas_endpoint()
#	print(test)
#if __name__ == '__main__':
#	appsheet2firebase()

port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
	app.run(threaded=True, host='0.0.0.0', port=port)


