# firebase2appsheet

#### Note: This is not an official Google Product. This is a demonstration for learning purposes only; it is not meant for a production deployment.

### Overview

- [Google Firestore](https://firebase.google.com/docs/firestore) is a fast, realtime nosql data store which also includes numerous API clients and entry points.

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) is an python, open-source web routing package that can handle all kinds of neat API scenarios.

- Google [Appsheet.com](https://www.appsheet.com) is a SaaS platform for no-code mobile applications.

- [Google Cloud Run](https://cloud.google.com/run) creates production-grade containerized servers from your configured source code.

*This demo/solution combines all four of these elements. At the end of this demonstration you will have an Appsheet app which is connected to Firestore. This app will have some tables of data such as people, places, things and events.*

### Requirements

- Access to Google Cloud and a Google cloud project with billing enabled.
- Access to www.appsheet.com - registration is free.
- A general understanding of Google cloud projects as well as [cloud shell](https://cloud.google.com/shell).

- **If you have never done this particular pipeline before, we recommend [this tutorial](https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run) first.**

### Run it standalone

- If for whatever reason, you want to run this flask server on your local machine, here are the quick notes:
	- It's python 3.
	- We make no assumptions about python virtual envs or module support.
	- It's pretty straightforward and should work if you are familar with python.
	- You will need to paste in your key.json file from Google IAM into "misc/key.json" file of this project.

- The default for this example is to run on localhost:8080 and misc/oas.yml refers to this URL. In a later step below, after we deploy to cloud run, we will run a curl command to "init" the instance as well as change the OAS server url to match our new cloud run hostname.

- The rest of these instructions are canned and tutorialized and should work as-is. Please let us know if not.

### High Level Steps - Google Firestore

- Sign up for [Google Firebase](https://console.firebase.google.com/) and create a new project. The project name is up to you - we chose "appsheet-firestore" for our example:

![create_firestore.png](media/create_firestore.png)

- You can disable google analytics for this demonstration:

![create_firestore2.png](media/create_firestore2.png)

- Once your project is up and running, create a new Firestore Database:

![create_firestore3.png](media/create_firestore3.png)

- For security purposes, we recommend Production Mode:

![create_firestore4.png](media/create_firestore4.png)

- For Firestore Location, we chose us-central:

![create_firestore5.png](media/create_firestore5.png)

- Once the database is created, click on Project Settings, then Service Accounts. Then click "Generate new private key" and download your JSON file. You will need this json file later:

![create_firestore6.png](media/create_firestore6.png)

### High Level Steps - Google Cloud Run

- Open a new tab and go to [https://console.cloud.google.com/](https://console.cloud.google.com/). In the steps above, Firestore created a Google Cloud Project for you. Make sure that is selected:

![cloud_run.png](media/cloud_run.png)

- We need to enable the Cloud Run API. You can search for this at the top of your project:

![cloud_run1.png](media/cloud_run1.png)

- Enabling this API will take a moment. We also need to add two roles to the Cloud Build Account. Navigate to IAM, find the account that has the words "cloudbuild" in it, click the pencil icon, and add these two roles:

![cloud_run1.png](media/cloud_iam.png)

- Once the above is complete, now search for "Cloud Run" to navigate to this part of the console. Then, open up the cloud shell. This may take a moment:

![cloud_run2.png](media/cloud_run2.png)

- Download this very github project to your Google cloud shell and also execute a few other commands as follows:
	- `git clone https://github.com/northwestcoder/firebase2appsheet`
	- `cd firebase2appsheet`
	- `echo -n "mylongapikey123890sdflkjw45" > misc/apikey`

![cloud_run3.png](media/cloud_run3.png)

- The last command above creates a new api key for later use in Appsheet. You will need to take note of this key (and you can change the value as desired)

- Next, open up the cloud editor, find the file key.json and paste in the entire contents of the JSON file you downloaded during the Firestore configuration.

![cloud_run4.png](media/cloud_run4.png)

- **Save your changes!** Now go back to cloud shell mode (you will now probably have noted that there is a toggle button between "Open Editor" and "Open Terminal").

- We will need to run cloud build **twice**
	- The first time is to creat the cloud build which gives us a proper DNS and hostname
	- We will then edit our ./misc/oas.yml file and change the URL to this new DNS
	- And then we will run cloud build a second time to update the container.

- Run cloud build the first time
	- You will also be prompted to Authorize Cloud Shell.
	- If you get errors, it means one or more of the steps above are incomplete.

`gcloud builds submit --config cloudbuild.yaml .`

- Don't forget the trailing period (".") in the above command. The build will take a few minutes. Cloud run will nicely wrap this python flask server running on http/8080 into a new containerized instance running on https/443. At the end you should see "success" as well as your new hostname:

![cloud_run5.png](media/cloud_run5.png)


- Copy the new app URL that is displayed at the end of the build. You can even try to open a browser to <THENEWURL>/events, and you should get "Unauthorized" - this is because you didn't provide an API key and indicates success.

- Now go back into EDITOR mode, find the file `./misc/oas.yml`, and change the URL entry to the new App URL from above. Include the trailing slash. Save your changes when done: 

![cloud_run6.png](media/cloud_run6.png)

- Go back to the shell and run the build a second time:

`gcloud builds submit --config cloudbuild.yaml .`

- If you are an OpenAPI expert, you might now notice that:
	- Storing our oas.yml inside the server container which is running the endpoints is a brittle way to manage openapi specs. 
	- But from a demo perspective or single-deployment perspective, we're ok :) 
	- Also if your goal is simply to expose Firestore to Appsheet, then this procedure is potentially valid for production. 

- If everything worked out OK, now we are ready to use Appsheet.com

### High Level Steps - Google Appsheet

- Go to www.appsheet.com, sign in and/or register, and create a new Rest API connection ("Apigee") using this endpoint: `https://YOURNEW_APP_URL/oaspec` and using the apikey you configured above - for more information on the rest API connector in Appsheet go [here](https://help.appsheet.com/en/articles/4438873-apigee-data-source).

![appsheet.png](media/appsheet.png)

- Don't forget the trailing "oaspec". You need to click "validate" and then "authorize access"

- Now copy the appsheet template that we have provided: [template Appsheet app](https://www.appsheet.com/samples/Companion-app-for-a-github-project-See-About--More-Information?appGuidString=9729275d-1821-46fb-bc90-031222d77413) which is currently using Google Sheets.

![appsheet2.png](media/appsheet2.png)

- Click "copy and customize". On the next screen give it a name, check the box for "copy data" and wait a few minutes while it copies into your Appsheet account:

![appsheet3.png](media/appsheet3.png)

- When your new copy of the template app comes up, you will need to REPLACE each google sheet connection with your new (apigee) Rest API connection. For example, navigate to the "persons" table and choose "browse for more data":

![appsheet4.png](media/appsheet4.png)

- And then select your new Rest API datasource, and then the "persons" table:

![appsheet5.png](media/appsheet5.png)

- Repeat this for every data source in this app (people, places, things, events, settings, contents), *except for* the "help" and "globals" tables. These datasources will remain as google sheets.

- Once complete, you should see one person, one place, one thing, and one event. 

- *There's a glitch or bug in Appsheet as of this writing*: for each of our new API-driven tables, you need to:
	- "Regenerate column structure"
	- delete the newly created virtual column "ComputedKey"
	- re-enable the "id" field as the key field.
	- You need to do this for each of persons, events, places, things, contents, and settings.
	- sorry about that :( 

- *Another Glitch: all of the various "photo" fields might get marked as type "URL" when you copy the app.* In the column grid editor for each table, you need to change these "photo" fields to type "image" instead. Do this for people, places, things, and events.

- Now let's bulk-load some data. In the App itself, you can navigate to "People", and then click the upload icon:

![appsheet6.png](media/appsheet6.png)

- We have provided three CSV files in ./misc/appsheet* for people, places, and things. Repeat the above step for all three.

- Be patient, the app will update once the upload is complete. You can open your Firestore console and watch the data come into Firestore in realtime if you want!

- More Appsheet notes
	- Note that we are not storing any images in Firestore directly. Instead, when you first logged into Appsheet, you chose Google Auth or Microsoft Auth, and we are using those respective storage platforms for any uploaded images.
	- You can also download the Appsheet mobile app from the Apple or Google store and run this app on your smartphone. 

 **Congrats!**. Everything should be working now. You now have an end to end solution from Firestore to your no-code mobile app.

### Background

- We use Kaniko build images, check it out [here](https://github.com/GoogleContainerTools/kaniko#kaniko---build-images-in-kubernetes).

- In firebase, we created a simple data model of people, places, things, and events. There is also a special settings table.

- When you run the "/init" endpoint using curl above, it will try to create at least one record for each of these firestore collections:

	- persons
	- places
	- things
	- events
	- contents
	- settings

- Because this example assumes you are connecting with www.appsheet.com, there are thus all kinds of complications that we nicely avoid around oAuth, advanced OpenAPI Spec concepts, nested JSON in firestore, etc, etc.. Appsheet assumes that each firebase collection is a top-level "table" whose documents (children) are all *indentical in structure*. Because of this simplicity, there's a bunch of code-worrying that does *not* have to happen here.

- Appsheet - like a lot of clients - expects a flat table-esque structure. None of these Firestore examples have any nested JSON, and nor should they.

- Further, any time we are getting a collection of results in flask route code, we have to add the "tablename" to the JSON response like so ("events" is our table name):
```
jsonresult = jsonify({"events" : all_events}), 200
return jsonresult
```


- There's also a secret "heartbeat" setting which defaults to OFF. If set to ON, after 0-5 minutes, the cloud run instance will begin creating Firestore data once every five seconds, 30 times, and then will set heartbeat back to OFF. When OFF, the heartbeat checks Firestore every five minutes to see if someone has turned on the setting. Experimenting with this is left as an exercise for the reader. :)

### How to add your own tables

- You're going to need to dig into the code for this - we've tried to make it somewhat modular. 

- High level ideas

	- You'll need to edit oas.yml to reference your new table.
	- You'll want to make a copy of one of the route_*.py files, study it, and reference your new table accordingly.
	- You'll need to modify firebase2appsheet.py to reference your new route_*.py file.
	- You'll want to create an empty collection in Firestore for your data.
	- We might have missed something - please let us know!

- Template example

	- We have provided a route_yournewcollection file
	- This gets referenced in firebase2appsheet.py twice
		- an import statement
		- a blueprint statement
	- You would also need to edit your oas.yml, we recommend using a swagger editor.

- A note about timestamps

	- If you look in either route_events or route_yournewcollection, you will see that we set record "timestamp" (creation) and "lastmodified" dates.
	- We do so using *firestore server-side functions* for creation timestamp, but we allow Appsheet to send in "lastmodified".
	- The field "lastmodified" should be treated as a Datetime and can be marked as editable in Appsheet.
	- The field "timestamp" should be treated as a string and not editable in Appsheet. You can then create a virtual field which represents its value:
	
![timestamps.png](media/timestamps.png)

	- The premise here is to not allow the client to write timestamps, and instead have firestore do it. This way, all of our timestamps are universal and synchronized.


### How to productionize this Flask server

- We recommend removing all of the heartbeat code - that's just for demo purposes.

- Ditto for the initialization endpoint ("/init") - this is also just for demo purposes.

- We recommend splitting out the oas.yml file *away from* the containerized server.

- You can increase the memory footprint and change other settings of the containerized Cloud Run instance. Learn more [here](https://cloud.google.com/run/docs/configuring/memory-limits).

- For security: for this demo we baked in a file system "apikey" file. Since the goal for this solution is to act as a front end to Appsheet, and since you will be using Appsheet security and authentication in production, it's reasonable to leave this "apikey" solution in place. There are other possibilities here, such as adding python code to read from a google cloud secret, or similar steps.





