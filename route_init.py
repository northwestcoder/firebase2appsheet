from flask import Blueprint
from flask import request, jsonify
import re
from firebase_admin import firestore

import client
from apiauth import require_apikey

# initialize with one document per collection on each startup
# as a way to check for firestore collection existence

def initialdata():

    personref = client.db.collection('persons').document(u'abc123')
    personref.set({'id': 'abc123', 'Name': 'placeholder person abc123',  'active' : True, 
                'birthdate': '1970-04-04','email' : 'nobody@example.com', 'mobile' : '555-555-5555', 
                'photo': '', 'teams': 'Alpha Team , Bravo Team', 
                'tenure': 25})

    placeref = client.db.collection('places').document(u'abc123')
    placeref.set({'id': 'abc123', 'Name': 'placeholder place abc123',  'address' : '7200 Aurora Ave N, Seattle, WA 98103', 
                'latlong': '47.680584, -122.346198','mainline' : '555-555-5555', 'photo' : ''})

    thingref = client.db.collection('things').document(u'abc123')
    thingref.set({'id': 'abc123', 'Name': 'placeholder thing abc123',  'barcode' : '0123456789abcdef', 
                'startdate': '4/4/2020 12:00:00 AM','enddate' : '12/4/2021 12:00:00 AM', 'photo' : '', 'price' : 27.99, 
                'supplier' : 'Acme Supplies'})

    eventref = client.db.collection('events').document(u'abc123')
    eventref.set({'id': 'abc123', 'Name': 'placeholder event abc123', 'personid': 'abc123', 'placeid': 'abc123', 
                'thingid': 'abc123','eventtype' : 'party', 'timestamp' : firestore.SERVER_TIMESTAMP, 
                'duration': 1, 'address': '3051 NE 86th St, Seattle WA 98115', 
                'latlong': '47.680989, -122.303969', 
                'photo':'https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Google_Cloud_Covered.png', 
                'barcode': '0123456789abcdef', 'notes' : 'notes go here'})

    contentref = client.db.collection('contents').document(u'abc123')
    contentref.set({'id': 'abc123', 'content': 'placeholder content abc123'})

    settingsref = client.db.collection('settings').document(u'heartbeat')
    settingsref.set({'id': 'heartbeat', 'value': 'OFF'})


def replaceOAS_URL(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()


initroute = Blueprint('init', __name__)

@initroute.route('/init', methods=['POST'])
@require_apikey
def initializedata():


	newcloudrunurl = request.args.get('oas')
	
	try:
		initdata = initialdata()
		
		if newcloudrunurl is not None:
			replaceOAS_URL('misc/oas.yml','http://localhost:8080','https://'+newcloudrunurl)

		return jsonify({"success initializing this demo": True}), 200


	except Exception as e:
		return f"An Error Occurred creating new initial data: {e}"

