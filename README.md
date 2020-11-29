# firebase2appsheet

### Note: This is not an official Google Product.

### Requirements:

- Access to Google Cloud and a Google cloud project with billing enabled
- Access to www.appsheet.com - registration is free

- If you have never done this particular pipeline before, we recommend [this tutorial](https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run) first.


### High Level Steps

- Sign up for Google Firestore and create a new firestore project. The name is selectable - we chose "appsheet-firestore"

- Create a Google Cloud service account and JSON key. From console.firebase.com, click on project settings >> service Accounts >> manage Service Account permissions. This should redirect you to the Google IAM admin page. From here you want t ocreate a new service account and then generate a JSON key. We have deliberately avoided providing screenshots for this step because they keep changing how the UX looks :)

- The bottom line is you need a valid key.json file for use with this project :) 

- Download this project to your Google cloud shell, e.g. from your cloud shell home directory:

`git clone https://github.com/northwestcoder/firebase2appsheet`
`cd firebase2appsheet`

- create an empty file named *apikey* and make up an api key for later use, e.g. long alphanumerics, e.g.

`echo "mylongapikey-123890sdflkjw45" > apikey` - you will need this below.

- Paste your key.json contents into the empty key.json file provided (we used the Eclipse Theia cloud shell editor for this)

- Run cloud build:

`gcloud builds submit --config cloudbuild.yaml .`

- Cloud run will nicely wrap this python flask server running on http/8080 inside of a SSL instance running on https/443.

- Once build is complete, your endpoint is ready for use by Appsheet (or even postman at this point). Take note of the end point at the very end of the build steps, e.g.

`https://firebase2appsheet-{{randomid}}-uc.a.run.app/`

- in Appsheet.com, create a new Rest API connection ("Apigee") using this endpoint: 

`https://firebase2appsheet-{{randomid}}-uc.a.run.app/oaspec`



### Background

- We use Kaniko build images, check it out here:
https://github.com/GoogleContainerTools/kaniko#kaniko---build-images-in-kubernetes

- In firebase, we created a simple data model of people, places, things, and events. There is also a special settings table.

- when you fire up this client, it will try to create at least one record for each of these firestore collections:

	- persons
	- places
	- things
	- events
	- contents
	- settings

- because this example assumes you are connecting with www.appsheet.com there are all kinds of complications that we can avoid around oAuth, advanced OpenAPI Spec concepts, nested JSON in firestore, etc. Appsheet assumes that each firebase collection is a top-level "table" whose documents (children) are all *indentical in structure*. Because of this simplicity, there's a bunch of code worrying that does *not* have to happen...

