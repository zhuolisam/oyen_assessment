# Oyen Assessment

## Project Structure

```
oyen_internship
├─ .gitignore
├─ backend
│  ├─ .env
│  ├─ auth.py
│  ├─ crud.py
│  ├─ database.py
│  ├─ db
│  │  └─ database.db
│  ├─ main.py
│  ├─ models.py
│  ├─ requirements.txt
│  └─ schemas.py
├─ frontend
│  ├─ index.html
│  ├─ index.js
│  ├─ login.html
│  ├─ me.html
│  └─ signup.html
├─ README.md
└─ setup.sh

```

## How to Use
Clone this repo.

Use the `setup.sh full` command, it installs all the necessary dependencies.
```
# For Mac/Linux
sudo chmod 777 setup.sh
sh ./setup.sh full

#For Windows using Powershell
bash ./setup.sh full

```
The `full` argument spins up both frontend and backend server, if you wish to spin them up separately, run without the `full` argument, followed by this 
```
uvicorn main.app --reload
cd ..
python -m http.server 
python3 -m http.server 5000 --dir frontend

```

## Frontend
Exposed at `http://127.0.0.1:5000`
* Uses local storage to store jwt token.
* Protected page routing, eg: when a not logged in user visits home page, he will be redirect to login page and vice versa.

> In real life, we shall adhere to OAuth2.0 flow and open standards like OWASP. There should be a long live `refresh_token` in http-only cookie, and short live `access_token` in local storage.

## Backend
Exposed at `http://127.0.0.1:8000`
* Uses `jwt` token.
* Uses `bcrypt` to hash user password.
* `CORS` enabled.
* Separate modules, `crud.py` for db interaction, `models.py` for db ORM, `schemas.py` for type definition, `auth.py` for password hashing and jwt token encryption, `database.py` for db connection.
* Protected api route. In the `/me` endpoint that returns all login sessions of the current user, if there is no Bearer token presents in header that indicates the authorization of user, user would not get any data from it.

A sqlite database will be created in `db` folder after spinning up the server for the first time. 

All used libraries are listed in `requirements.txt`.

Please visit the SwaggerUI at `http.127.0.0.1:8000/docs` to test out all api endpoints.