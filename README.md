# demo-youtube-clone
Youtube Clone - Basic Level

This is a video sharing application based on Flask microframework which provides the main features of Youtube.

## Features

* Available now:
    * Users can upload videos(mp4 only). And edit the videos.
    * All visitors can watch videos and read users' profiles. 
    * All visitors can search videos based on titles.
    * Users can like/dislike a comment or a video.
    * Users can subscribe other users.
    * Users can reply to a video and a comment.
    * Users can edit profiles and password.
    * Users view liked videos and subscribed videos.

Unfortunately, I don't have time to fix some bugs in the app. Some frontend features are broken.

## Demo

I host the app on my own server. [Faketube](https://faketube.afai97202013.com)

The available accounts for the demo:

| Username | Password      |
|----------|---------------|
|Jon       |winteriscomming|
|Cersei    |imthequeen     |
|Gandalf   |youshallnotpass|

## Requirements

* Simple 
    * Docker Engine
    * Docker Compose


* Tradition
    * Python
    * Flask
    * Flask-SQLAlchemy
    * Flask-WTF
    * Flask-Login
    * SQL Database
    * WSGI Server (Optional)
    * Web Server (Optional)


## Usage

0. Copy the `env.example` to `.env`, which contains the environment variables for this app.

1. Clone this repo to your computer and run `docker-compose up --build` to create a image and launch the whole containers.

2. Run `docker-compose exec faketube flask db upgrade` to migrate the database.

3. And open your browser, then visit `localhost:8000`.

### TODO

* Feature:
    * Users can remove videos.
    * Users can remove comments.
    * Users can remove their accounts.
    * Users have to confirm their emails.
    * Add a dashboard for admin users.
    * Fix some bugs.
    * Users can process the videos not only mp4.

* System:
    * Deploy on Clouds, AWS or GCP.
    * Since the app has many static contents, videos and pictures, the CDN and file storage system are required.
    * Processing videos and sending Emails require a message queue and task queue system like RabbitMQ and Celery.
    * Divide the app into Frontend and Backend. Sever-side rendering, Jinga, is not well for scaling and I don't like the frontend works.

* Docker:
    * Better Dockerfile.
    * Publish the image to Docker Hub.
    * Deploy on Docker Swarm and Kubernetes.
