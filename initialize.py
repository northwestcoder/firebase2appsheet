from firebase_admin import firestore
import client

def initialize():

	settings = client.db.collection('settings')
	persons = client.db.collection('persons')
	places = client.db.collection('places')
	things = client.db.collection('things')
	events = client.db.collection('events')
	contents = client.db.collection('contents')

	# template that you can copy from
	yournewcollections = client.db.collection('yournewcollections')	

	if (len(settings.get())==0):
		print("generating first settings entry")
		new = settings.document(u'heartbeat')
		new.set({'id': 'heartbeat', 'value': 'OFF'})
	else:
		print("we have a settings collection already")



	if (len(persons.get())==0):
		print("generating first persons entry")
		new = persons.document(u'abc123')
		new.set({'id': 'abc123', 'Name': 'placeholder person abc123',  'active' : True, 
				'birthdate': '1970-04-04','email' : 'nobody@example.com', 'mobile' : '555-555-5555', 
				'photo': 'https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Google_Cloud_Covered.png', 
				'teams': 'Alpha Team , Bravo Team', 
				'tenure': 25})
	else:
		print("we have a person collection already")



	if (len(places.get())==0):
		print("generating first places entry")
		new = places.document(u'abc123')
		new.set({'id': 'abc123', 'Name': 'placeholder place abc123',  'address' : '7200 Aurora Ave N, Seattle, WA 98103', 
				'latlong': '47.680584, -122.346198','mainline' : '555-555-5555', 
				'photo' : 'https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Google_Cloud_Covered.png'})
	else:
		print("we have a places collection already")



	if (len(things.get())==0):
		print("generating first things entry")
		new = things.document(u'abc123')
		new.set({'id': 'abc123', 'Name': 'placeholder thing abc123',  'barcode' : '0123456789abcdef', 
                'startdate': '4/4/2020 12:00:00 AM','enddate' : '12/4/2021 12:00:00 AM', 
                'photo' : 'https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Google_Cloud_Covered.png',
                'price' : 27.99, 'supplier' : 'Acme Supplies'})
	else:
		print("we have a things collection already")



	if (len(events.get())==0):
		print("generating first events entry")
		new = events.document(u'abc123')
		new.set({'id': 'abc123', 'Name': 'placeholder event abc123', 'personid': 'abc123', 'placeid': 'abc123', 
                'thingid': 'abc123','eventtype' : 'party', 'timestamp' : firestore.SERVER_TIMESTAMP, 
                'duration': 1, 'address': '3051 NE 86th St, Seattle WA 98115', 
                'latlong': '47.680989, -122.303969', 
                'photo':'https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Google_Cloud_Covered.png', 
                'barcode': '0123456789abcdef', 'notes' : 'notes go here'})
	else:
		print("we have a events collection already")



	if (len(contents.get())==0):
		print("generating first contents entry")
		new = contents.document(u'abc123')
		new.set({'id': 'abc123', 'content': 'placeholder content abc123'})
	else:
		print("we have a contents collection already")


	# template that you can copy from
	if (len(yournewcollections.get())==0):
		print("generating first yournewcollections entry")
		new = yournewcollections.document(u'abc123')
		new.set({
			'id': 'abc123', 
			'Name': 'the name of this record', 
			'timestamp': firestore.SERVER_TIMESTAMP,
			'lastmodified': firestore.SERVER_TIMESTAMP, 
			'createdby': 'you@example.com', 
			'modifiedby': 'you@example.com', 
			'integervalue': 100,
			'floatvalue': 123.45, 
			'datevalue': '04/25/2020'
			})
	else:
		print("we have a yournewcollections collection already")





