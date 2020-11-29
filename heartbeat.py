import string
import random
import time
from datetime import datetime

from firebase_admin import firestore
import client

# event polling if heartbeat entry is set to ON

def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    uniqueid = ''.join(random.choice(chars) for _ in range(size))
    return uniqueid

def heartbeat():

	# don't start any of this until initializer.py has had time to create the setting...
	time.sleep(10)

	heartbeatstatus = client.db.collection(u'settings').document(u'heartbeat')
	status = heartbeatstatus.get().to_dict()["value"]

	while True:
		if (status == "ON"):	
			print("status is ON, we are in heartbeat mode")

			randomduration = random.randrange(25)
			recordid = id_generator()
			# lower left: 33.417827, -116.485679
			# upper right: 47.148747, -79.837476
			randlat = random.randint(33, 47)
			randlong = random.randint(-116,-79)
			randomlatlong = str(randlat) + ", " + str(randlong)
			randomimageurl = "http://ipsumimage.appspot.com/300?s=60&f=000000&b=CCCCCC&l=" + recordid

			try:
				ping = {'id': recordid, 'Name': 'heartbeat event ' + recordid, 'personid': 'abc123', 'placeid': 'abc123', 
				'thingid': 'abc123','eventtype' : 'heartbeat', 
				'duration': randomduration, 'address': '3051 NE 86th St, Seattle WA 98115', 
				'latlong': randomlatlong, 'photo': randomimageurl, 'barcode': '0123456789abcdef', 'notes' : 'some notes go here..',
				'timestamp':firestore.SERVER_TIMESTAMP}
				client.db.collection(u'events').document(recordid).set(ping)

				heartbeatstatus = client.db.collection(u'settings').document(u'heartbeat')
				status = heartbeatstatus.get().to_dict()["value"]
				time.sleep(5)
			except Exception as e:
				time.sleep(5)
				return f"An Error Occurred: {e}"
		else:
			print("status is OFF, heartbeat mode paused")	
			heartbeatstatus = client.db.collection(u'settings').document(u'heartbeat')
			status = heartbeatstatus.get().to_dict()["value"]
			time.sleep(300)