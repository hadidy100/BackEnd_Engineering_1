# BackEnd_Engineering_1

A Web Service API for a discussion forum application.
 
The application should exposes the following RESTful URL endpoints. All data sent to and from the API should be in JSON format with the Content-Type header field set to application/json.


<h1>Instructions:</h1>
initialize drop,create database tables and using test data with sql script:
<p><font color="green">flask init_db</font></p>

test GET,POST,PUT,etc... using the following curl commands:
<p><font color="green">curl -i http://localhost:5000/forums</font></p>
<p><font color="green">curl -u david:password -i -d '{"name":"cassandra"}' -H "Content-Type: application/json" -X POST "http://localhost:5000/forums"</font></p>
<br><br>



Method
GET
URL
/forums
Action
List available discussion forums
Request Payload
N/A
Successful Response
HTTP 200 OK
[
    { "id": 1, name: "redis", creator: "alice" }
    { "id": 2, name: "mongodb", creator: "bob" }
]
Error Response
None. Returns an empty array if no forums have been created.
Requires Authentication?
No


Method
POST
URL
/forums
Action
Create a new discussion forum
Request Payload
{
    "name": "cassandra"
}
Successful Response
HTTP 201 Created

Location header field set to /forums/<forum_id> for new forum.
Error Response
HTTP 409 Conflict if forum already exists
Requires Authentication?
Yes
Notes
Forum’s creator is the current authenticated user.


Method
GET
URL
/forums/<forum_id>
Action
List threads in the specified forum
Request Payload
N/A
Successful Response
HTTP 200 OK
[
    {
        "id": 1,
        "title": "Does anyone know how to start Redis?",
        "creator": 'bob',
        "timestamp": "Wed, 05 Sep 2018 16:22:29 GMT"
    },
    {
        "id": 2,
        "title": "Has anyone heard of Edis?",
        "creator": "charlie",
        "timestamp": "Tue, 04 Sep 2018 13:18:43 GMT"
    }
]
Error Response
HTTP 404 Not Found
Requires Authentication?
No
Notes
The timestamp for a thread is the timestamp for the most recent post to that thread.

The creator for a thread is the author of its first post.

Threads are listed in reverse chronological order.


Method
POST
URL
/forums/<forum_id>
Action
Create a new thread in the specified forum
Request Payload
{
    "title": "Does anyone know how to start MongoDB?",
    "text": "I'm trying to connect to MongoDB, but it doesn't seem to be running."
}
Successful Response
HTTP 201 Created

Location header field set to /forums/<forum_id>/<thread_id> for new thread.
Error Response
HTTP 404 Not Found
Requires Authentication?
Yes
Notes
The "text" field becomes the first post to the thread. The first post’s author is the current authenticated user.


Method
GET
URL
/forums/<forum_id>/<thread_id>
Action
List posts to the specified thread
Request Payload
N/A
Successful Response
HTTP 200 OK
[
    {
        "author": "bob",
        "text": "I'm trying to connect to MongoDB, but it doesn't seem to be running.",
        "timestamp”: "Tue, 04 Sep 2018 15:42:28 GMT"
    },
    {
        "author": "alice",
        "text": "Ummm… maybe 'sudo service start mongodb'?",
        "timestamp”: "Tue, 04 Sep 2018 15:45:36 GMT"
    }
]
Error Response
HTTP 404 Not Found
Requires Authentication?
No
Notes
Posts are listed in chronological order.


Method
POST
URL
/forums/<forum_id>/<thread_id>
Action
Add a new post to the specified thread
Request Payload
{
    "text": "@Bob: Derp."
}
Successful Response
HTTP 201 Created
Error Response
HTTP 404 Not Found
Requires Authentication?
Yes
Notes
The post’s author is the current authenticated user.


Method
POST
URL
/users
Action
Create a new user
Request Payload
{
    "username": "eve",
    "password”: "passw0rd"
}
Successful Response
HTTP 201 Created
Error Response
HTTP 409 Conflict if username already exists
Requires Authentication?
No


Method
PUT
URL
/users/<username>
Action
Changes a user’s password
Request Payload
{
    "username": "eve",
    "password”: "s3cr3t"
}
Successful Response
HTTP 200 OK
Error Response
HTTP 404 Not Found if username does not exist

HTTP 409 Conflict if "username" field does not match the current authenticated user.
Requires Authentication?
Yes
Authentication
Use HTTP Basic authentication to authenticate users. You may implement this yourself, or install the Flask-BasicAuth extension.
To use Flask-BasicAuth, create a subclass of flask.ext.basicauth.BasicAuth and override its check_credentials method to read from the database instead of comparing to the BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD configuration variables.
