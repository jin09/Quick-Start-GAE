# Webapp2 With App Engine SDK

Developer can leverage the App Engine services as well eg. Datastore, Memcache etc.

## PORT

Default Port for application is `8080`. 

## Docker Run Procedure

Make sure docker is installed, if not : 

`sudo apt-get install docker.io`

Build the project : 

`sudo docker build .`

Run the built image (always available app --restart flag): 

`sudo docker run -d -p 5000:8080 --restart always [IMAGE_ID_OF_PREVIOUS_BUILD]`

Now you can access this app on 

`localhost:5000`

## Stop Current Deployment

Update the container restart properties

`sudo docker update --restart=no [Container-ID]`

Stop the running container

`sudo docker stop [Container-ID]`

Pull the latest changes and repeat this procedure to deploy the latest version of this app 


