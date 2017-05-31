# API

## Notes
* See [tests](tests.rest) for request examples.
* Remember to place an ending slash in request uri.

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
```

### Yet unimplemented
```
GET /user/<username>/<app>/
	returns user <username>'s stats concerning <app> usage
POST /user/<app>/
	with auth
	creates new session
	returns session id
PUT /user/<app>/
	with payload: {finished: <has_finished>}
	session heartbeat
	if (<has_finished>) stops current session
```
