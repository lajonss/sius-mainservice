# API

## Notes
* See [tests](./tests.rest) for request examples.
* Remember to place an ending slash in request uri.
* Example time format: "2017-05-31T23:00:00"

## Running dev server
```
git checkout develop
export MAINSERVICE_DB_PASSWORD=<db password>
python manage.py runserver
```

## Running in prod
### Preparation
```
git checkout master
```
#### Static files generation
```
python manage.py collectstatic
```
Static assets will be available in build directory.
#### Configuration
Check [nginx.conf](./nginx.conf) for proposed configuration. Remember to change static files directories to your liking.
### Running
```
export MAINSERVICE_DB_PASSWORD=<db password>
gunicorn mainservice.wsgi -b 127.0.0.1:8998
sudo systemctl start nginx
```
