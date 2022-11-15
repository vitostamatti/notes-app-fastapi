

<h1 align="center">Notes App FastAPI</h1>


<p align="center"> 
    A basic CRUD API of Notes with users JWT authentication.
    <br> 
</p>


## Getting Started <a name = "getting_started"></a>

First you need to clone this repository.

```bash
git clone https://github.com/vitostamatti/notes-app-fastapi/ 
```

Then cd into the notes-app-fastapi directory and run 

```
docker compose up
```

If you don't have docker installed you first need to [download](https://www.docker.com/) it.

## Usage <a name="usage"></a>

When the docker containers are running you can start playing with the app.

If you go to [localhost/5050](http://localhost/5050) you're going to see the pgadming app. 
There you can login using: 
- username: admin@domain.com 
- password: admin 

The best way to interact with the api listening on [localhost/8000](http://localhost/8000) 
is to access going to [localhost/8000/docs](http://localhost/8000/docs) and play around 
with the swagger documentation. To login as a superuser use:

- username: admin
- password: admin

You'll get a bearer token in theresponse and this will provide access to the rest of the endpoints.


## Authors <a name = "authors"></a>

- [@vitostamatti](https://github.com/vitostamatti) - Idea & Initial work


