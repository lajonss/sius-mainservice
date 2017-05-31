# API

## Notes
* See [tests](https://raw.githubusercontent.com/lajonss/sius-mainservice/master/tests.rest) for request examples. Link points to raw version because of Github's format misinterpretations.
* Remember to place an ending slash in request uri.
* Example time format: "2017-05-31T23:00:00"

## Endpoints

```
POST /rest-auth/login/
	with payload: {"username": <username>, "password": <password>}
	returns auth token
GET /user/<username>/
	returns all apps used by user <username>
POST /user/
	with payload: <appname>
	with auth
	links app <appname> with authenticated user
GET /app/<appname>/
	returns app <appname> global stats
POST /app/
	with payload: {"name": <appname>}
	with auth
	adds new app (global)
POST /user/app/<appname>/
	with payload: {"start_time": <time>}
	with auth
	starts new session
PUT /user/app/<appname>/
	with payload: {"notes"(optional): <notes>, "rating"(optional): <rating>}
	with auth
	updates user's app metadata
GET /user/<username>/<appname>/
	returns user <username>'s <appname> sessions
PUT /user/<appname>/session/
	with auth
	with payload: {"end_time": <time>}
	updates current session
DELETE /user/<appname>/session/
	with auth
	with payload: {"end_time"(optional): <time>}
	ends current session
```

### Unimplemented yet
```
None for now.
```
