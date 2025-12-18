# SafeTrek
### This project was built by Monash University's FIT students under the Industry Experience Studio Project unit (FIT5120)

SafeTrek is an interactive web platform that juxtaposes road crash data with vehicle, weather, and road condition variables on top of convenient and intuitive geographic visualizations to provide a powerful decision-support tool to city planners and policymakers.

At a high-level, the system shall:

- Aggregate and process open crash datasets from trusted government sources.

- Provide interactive heatmaps and dashboards showing risks at the SA2 level, and eventually at the road/street level.

- Allow users to filter by demographic (e.g., age, gender), vehicle type, weather, or time-of-day to uncover correlations.

- Highlight "blackspots" and areas of recurring high risk.

- Apply an equity lens to reveal which groups or communities are disproportionately impacted.

This solution empowers decision-makers with data-driven insights, enabling them to design safer, fairer, and more effective interventions.

## Technical Implementation Details

### Overall structure
We have each component of the system running as a docker container (service), and docker-compose.yml (deprecated) and docker-compose-native.yml files at the root directory of the project are responsible for running the whole system on local machines and/or on cloud instances. The docker-compose-native.yml file would build the necessary images locally using the dockerfiles defined in each service's subdirectory, and a shell script called "cloud_deploy.sh" is provided for convenience, which is responsible for building and running all the essential services on a cloud environment (e.g, EC2 instance) along with 2 additional services that handle SSL certification and HTTP to HTTPS redirection

The following components of the system are defined as docker services inside the outermost docker-compose-native.yml:
- Backend (Python + FastAPI and other libraries for communicating with the database and other associated services)
- Frontend (VueJS powered by Leaflet by OpenStreetMaps for geographic visualizations)
- Database (PostGreSQL with PostGIS)
- Nginx (A proxy server to handle SSL certification)

The docker-compose-cloud.yml builds the images for these services locally on a given PC or cloud instance (such as AWS EC2). While the backend, frontend and database services are self-explanatory, we build and run 2 additional services to facilitate SSL certification and hence allow HTTPS traffic, namely:
- "nginx-proxy" which pulls from jwilder/nginx-proxy and uses the default.conf file in our filetree, and 
- "letsencrypt" which pulls from jrcs/letsencrypt-nginx-proxy-companion and generates SSL certificates based on the domain name specified in cloud.env. The domain name here should match the same in default.conf.

## Building & Running Locally

### Initial Setup

Before being able to build/run the whole system the very first time on a given PC, you will need to follow some preliminary steps to ensure the database service is populated.

#### Data

Follow the instructions in data/instructions.md to download and unzip the necessary data, but DON'T run `docker compose up -d` there as instructed in that file unless you wish to spin up the database docker service in a standalone form. Just unzip the files/folders as instructed after downloading the zip file, and the database service will be created and populated while building the whole system natively as described soon.

### Building & Running Locally

Building and running the whole system with all the necessary components locally is fairly simple and straightfoward once you have finished the initial setup - all you really need is docker installed (and the daemon must be running), along with all the relevant user permissions (typically achieved by adding the currently logged-in user to the docker usergroup on UNIX-like machines).

Just run
`docker compose up -d --build`
on a terminal/command-line window inside the root folder of this repository (the folder containing this readme file) and wait for all the components to be built and started as docker services.

IMPORTANT: The very first time you run this setup on a given PC, the system will not be operational as soon as all the docker services are started, since the database service (`postgis`) will need some time to read data. You can check the status of this service this way:

1. Run `docker ps` on a terminal/command-line window, you should see a list of all running docker services, for example:
    CONTAINER ID   IMAGE               COMMAND                  ... [other fields]
    4250a2a47291   safetrek-frontend   "/docker-entrypoint.s..."   ...
    1e1471736204   safetrek-backend    "uvicorn main:app --..."   ...
    46e779fb4f64   safetrek-postgis    "docker-entrypoint.s..."   ...

2. Note the first 2-3 characters of the container ID of the `safetrek-postgis` service - in our example, it would be 46e - and run `docker logs -f <first few characters of the postgis container's ID>` - in our case, it would be `docker logs -f 46e`

And you should be able to see the logs of the docker container running the PostGIS database - the very first time, you should be seeing PostGreSQL logs such as `CREATE TABLE ...` or `ALTER TABLE ...` or similar for a few minutes, this indicates that the database is still being built using the files you unzipped earlier. Wait for the PostGreSQL operations to be completed, at the end you should see "The database is ready to accept connections", at which point, you can begin testing the system by opening a browser window and going to `localhost` or `localhost:80`.

### Bringing Down The System
To stop the whole system, simply run `docker compose down` in the root directory of this repository.
In order to delete all data, in addition to deleting this repository and the downloaded data zip file earlier, you should also list all docker images, containers, and other resources if any and delete everything associated with safetrek - all our images contain the word `safetrek` or `strek` as part of their names.
