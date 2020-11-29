import os
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()


def getapikey():
	try:
		api_key_value = open('apikey', 'r').read()	
		return api_key_value
	except Exception as e:
		return f"An Error Occurred reading oas spec: {e}"


