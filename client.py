import os
from firebase_admin import credentials, firestore, initialize_app

# 1. our initializer 'db' which is called by the rest of the app.

# I'm not sure if firestore client should be a single global instance var, or called each time as needed.
# pretty sure it's the latter..

cred = credentials.Certificate('misc/key.json')
default_app = initialize_app(cred)
db = firestore.client()

# 2. remember folks, this is a demo and reference build
# it's ok for us to read the file system for each request that comes in
# in fact, possibly desirable for testing purposes...
# but in production you would probably not want to do this.

def getapikey():
	try:
		api_key_value = open('misc/apikey', 'r').read()	
		return api_key_value
	except Exception as e:
		return f"An Error Occurred reading api key on file system: {e}"

instance_apikey = getapikey()
