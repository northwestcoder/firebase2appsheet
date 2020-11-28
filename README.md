# firebase2appsheet




high level

we use Kaniko build images, check it out here:
https://github.com/GoogleContainerTools/kaniko#kaniko---build-images-in-kubernetes



-- create a firestore and two collections, "persons" and "events"
-- create a google cloud func for this codeline


-- create file key.json and populate with your auth key from firebase, else fail

-- run cloud build

gcloud builds submit --config cloudbuild.yaml .


