# OmahTI-BackEnd-oprec

#turning on the server (in the directory that has the main.py file)
cd python main.py

* Running on http://127.0.0.1:5000

* Testing RESTFul API using Postman

#Registering a new user
- Method: POST
- URL: http://127.0.0.1:5000/register
- Body (raw):
  {
    "username": "satyabudi",
    "password": "1l0v3c0d1ng"
}
- If successful, return code 201 and message "User created successfully!"
- If not, return code 400 and message "User already exists!". Return 500 if server error.

#Loging in as a registered user
- Method: POST
- URL: http://127.0.0.1:5000/login
- Body (raw):
  {
    "username": "satyabudi",
    "password": "1l0v3c0d1ng"
}
- If successful, return code 200 and the token.
- If not, return code 400 and message "Invalid credentials"

#Creating a new video
- Method: POST
- URL: http://127.0.0.1:5000/video
- Authorization: Basic Auth:
Username: satyabudi
Password: 1l0v3c0d1ng
- Content-Type: application/json
- Body (raw):
  {
  "name": "My First Video",
  "views": 100,
  "likes": 10
}
- If successful, return code 201 and a video id.
- If not, return code 400 and message "Missing required fields"

#Retrieving a video
- Method: GET
- http://127.0.0.1:5000/video/1


  
