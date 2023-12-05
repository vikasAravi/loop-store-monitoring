How to set up the project? 

1. Install the Docker and start the Docker. 
2. Clone the Repository. 
3. Under the project folder, run the below commands ( this folder where we are running the docker commands should have Dockerfile, docker-compose.yml file )
  3.1 docker-compose down
  3.2 docker-compose build
  3.3 docker-compose up  
4. The above commands start the resources which are required for the app.
5. Install all the dependencies ( python ) => pip3 install -r requirements.txt

6. Choose the current Directory as an app ( which is under the project ) => cd /app
7. Run the main file which will start the FastAPI app and the Cron ( If the python3 main.py won't work, either provide the absolute path / add the path to system variables ) 
8. Run the consumer by choosing the current directory ( path => <project>/app/consumers ) => python3 main.py and it will initiate the consumers. 


NOTE 

1. Using Local MongoDB ( Can refer to clients folder )
2. Using Local Kafka ( Can refer to client folder )
3. store_app => All the store-related handlers
4. store_monitoring_app => All the store Monitoring request handlers


API Documentation - http://0.0.0.0:8000/docs ( Change the host and port accordingly ) 
