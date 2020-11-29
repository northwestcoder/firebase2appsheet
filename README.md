# firebase2appsheet

### Note: This is not an official Google Product.

### Requirements:

- Access to Google Cloud and a Google cloud project with billing enabled
- Access to www.appsheet.com - registration is free

- If you have never done this particular pipeline before, we recommend [this tutorial](https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run) first.


### High Level Steps - Google Firebase and Cloud Run

- Sign up for Google Firestore and create a new firestore project. The name is selectable - we chose "appsheet-firestore"

- Create a Google Cloud service account and JSON key. From console.firebase.com, click on project settings >> service Accounts >> manage Service Account permissions. This should redirect you to the Google IAM admin page. From here you will need to create a new service account and then generate a JSON key. We have deliberately avoided providing screenshots for this step because they keep changing how the UX looks :) the bottom line is you need a valid key.json file for use with this project.

- Download this very github project to your Google cloud shell, e.g. from your cloud shell home directory:

`git clone https://github.com/northwestcoder/firebase2appsheet`

`cd firebase2appsheet`

- create an empty file named *apikey* and make up an api key for later use, e.g. long alphanumerics. You will need this in a future step below. Storing api keys in a container like this is fragile and should only be used for testing.


`echo -n "mylongapikey-123890sdflkjw45" > apikey`

- Paste your key.json contents into the empty key.json file provided (we used the Eclipse Theia cloud shell editor for this). Same comment as previous step regarding fragility.

- Run cloud build:

`gcloud builds submit --config cloudbuild.yaml .`

- Cloud run will nicely wrap this python flask server running on http/8080 inside of a SSL instance running on https/443.

- Once build is complete, your endpoint is ready for use by Appsheet (or even postman at this point). Take note of the end point at the very end of the build steps, e.g.

`https://firebase2appsheet-{{randomid}}-uc.a.run.app/`

### High Level Steps - Google Appsheet

- in Appsheet.com, create a new Rest API connection ("Apigee") using this endpoint: 

`https://firebase2appsheet-{{randomid}}-uc.a.run.app/oaspec`

using the apikey you configured - you also need to change *randomid* above according to your cloud build URL. For more information on the rest API connector in Appsheet go [here](https://help.appsheet.com/en/articles/4438873-apigee-data-source) 

- We have also provided a [template app](https://www.appsheet.com/samples/Companion-app-for-a-github-project-See-About--More-Information?appGuidString=4615279d-6ace-4adb-8eda-241bdf692bdc) which is currently using Google Sheets. The premise here is that if you were successful in following all of the instructions above, you can swap out - one by one - each table reference in this template app, from Google Sheets to your newly configured rest API data source.

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

- Because this example assumes you are connecting with www.appsheet.com, there are thus all kinds of complications that we nicely avoid around oAuth, advanced OpenAPI Spec concepts, nested JSON in firestore, etc, etc.. Appsheet assumes that each firebase collection is a top-level "table" whose documents (children) are all *indentical in structure*. Because of this simplicity, there's a bunch of code-worrying that does *not* have to happen here.

- There's also a secret "heartbeat" setting which defaults to OFF. If ON, the cloud run instance will create Firestore data once a minute. Enabling this is left as a fun challenge for the reader. :)
