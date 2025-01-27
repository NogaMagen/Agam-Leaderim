How to run-

First- cd to the docker directory. 

Second run the command- docker-compose up --build
the routes are going to be on http://127.0.0.1:8000/docs#/

Database Population Guide
---Important: Populate is a function in the api (the db save the information) - 
so the cvs files will not populate the db everytime the app start.  



adding a client you can run separately-


from datetime import datetime, timedelta, timezone

import requests
from jose import jwt

SECRET_KEY = "agam-leaderim"
ALGORITHM = "HS256"


def create_test_token():
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "sub": "test_user",
        "exp": expire.timestamp(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


access_token = create_test_token()

url = "http://localhost:8000/populate_employers"
headers = {"Authorization": f"Bearer {access_token}"}
params = {"search_term": "noga"}

response = requests.get(url, params=params, headers=headers)
print(response.status_code, response.json())
