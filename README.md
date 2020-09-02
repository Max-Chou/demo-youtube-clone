# demo-youtube-clone
Youtube Clone - basic version

This is a video sharing application based on Flask microframework which provides the main features of Youtube.

**Warning - This app is only for my portfolio, so don't use it for production.**

## Features

* User Login and Authentication
* Upload vidoes
* Search vidoes
* Subscribe Users
* Comment and Reply
* Like or Dislike comments and videos


## Setup

* Docker Engine
* Docker Compose

The application can be run in Linux systems with python and flask installed. I suggest run it by Docker Engine because it's easy and save you lots of troubles.


## Usage

Clone this repo to your desktop and run `docker-compose up --build` which will create a web image and launch an app and a database container.
And make a new `.env` by copying the `env.example`. The file contains the environment variables for this app. 

If you successfully launch the web container and database container, open your browser and visit `localhost:8000`.


## demo

[Faketube](https://faketube.afai97202013.com)

**Test Accounts**

* Username: Jon Password: winteriscomming
* Username: Cersei Password: imthequeen
* Username: Gandalf Password: youshallnotpass


You cannot signup or change the password on this demo.


## Notes for developers


### Stacks 

* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Flask-WTF
* Flask-Login
* PostgreSQL(pro-db)

I don't want to use too much extensions in this app. Just keep things simple.


### TODOS (If I have time to do...)

1. User's Email confirmation and password reset (Need a SMTP server or a Mail service)

2. Update Profile Pictures.

3. Delete Videos, Comments, and Replies. Edit Comments and Replies.

4. History (Record user's behaviors, add another user models)

5. Number of Views (Record user's behaviors, identify unique user?)

6. Better Performances (Tricky)

7. Monitor 

8. Testing


### Database Schema
![Database Schema](/schema.png)

### Rest API

Comming Soon...


### Deployment

#### Server
Comming Soon...



#### Container
Comming Soon...
