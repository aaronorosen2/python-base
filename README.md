# Django

```
DEV start

docker-compose -f docker-compose-dev.yml up
```


## Build project

```
docker-compose build
```

## Running for debug mode
```
docker-compose run --service web
```

## Start app
```
docker-compose run web python3 manage.py startapp <APPNAME>
```
