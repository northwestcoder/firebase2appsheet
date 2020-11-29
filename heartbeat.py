import string
import random
import time
from datetime import datetime

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

			recordid = id_generator()
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S %p")
			print(now)
			try:
				ping = {'id': recordid, 'Name': 'heartbeat event ' + recordid, 'personid': 'abc123', 'placeid': 'abc123', 
						'thingid': 'abc123','eventtype' : 'party', 'timestamp' : dt_string, 
						'duration': 3, 'address': '3051 NE 86th St, Seattle WA 98115', 
						'latlong': '47.680989, -122.303969', 'photo':'', 'barcode': '', 'notes' : ''}
			
				client.db.collection(u'events').document(recordid).set(ping)
				heartbeatstatus = client.db.collection(u'settings').document(u'heartbeat')
				status = heartbeatstatus.get().to_dict()["value"]
			except Exception as e:
				return f"An Error Occurred: {e}"
		else:
			print("status is OFF, heartbeat mode paused")	
			heartbeatstatus = client.db.collection(u'settings').document(u'heartbeat')
			status = heartbeatstatus.get().to_dict()["value"]
		time.sleep(5)