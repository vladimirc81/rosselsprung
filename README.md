# Running Rosselsprung with Docker Compose 

First we need to 'clone' repository with command:

```
git clone https://github.com/vladimirc81/rosselsprung.git
cd rosselsprung
```

After this - we start docker-compose command with:

```
docker-compose up -d --build
```

This command would build images (if they are not allready in docker images)
and run as daemon - exposing ports 80 and 5432

if we have images (app and ratestask) in our docker images we run:

```
docker-compose up -d
```

In case there is need to view output from containers we just run:

```
docker-compose up
```


After we finish running container we can shutdown with:

```
docker-compose down
```



# REST API 
Description:
METHOD GET - used for searching avg prices between two ports. We have origin and destination
This metod use: /v1/rates/<date_from>/<date_to>/<origin>/<destination>/ 

METHOD POST - used for insertion prices into DB. For this method we can only use code. 
This method use: /v1/rates/<date_from>/<date_to>/<orig_code>/<dest_code>/<int:price>/


METHOD GET - search avg prices

We want to view avg prices for each day , origin port CNGGZ - destination port EETLL

```
curl -X GET http://127.0.0.1/v1/rates/2016-01-01/2016-01-02/CNGGZ/EETLL/
```
Response:
```json
[
    {
        "day": "2016-01-01",
        "average_price": 1154
    },
    {
        "day": "2016-01-02",
        "average_price": 1154
    }
]
```


We can use code or parent_slug 
```
curl -X GET http://127.0.0.1/v1/rates/2016-01-01/2016-01-04/CNGGZ/north_europe_sub/
```
Response:
```json
[
    {
        "day": "2016-01-01",
        "average_price": 1532
    },
    {
        "day": "2016-01-02",
        "average_price": 1532
    },
    {
        "day": "2016-01-03",
        "average_price": 1532
    },
    {
        "day": "2016-01-04",
        "average_price": 1531
    }
]
```

METHOD POST - insert prices into db

If we want to updated our DB with prices:
```
curl -X POST http://127.0.0.1/v1/rates/2017-01-01/2017-02-03/CNGGZ/EETLL/123/
```
Response:
```json
{
  "Ok": "Ok"
}
```

Keep in mind we can not use parent_slug as in METHOD GET. 


# ERROR response

Error handling was done proper way. Each know error would be printed in json. 
If happen that code crash - it would report HTTP 500 (server side issue)

# How we insert DB ? 

Inside of app.py there is check for 'ratestask' postgresql and tables (ports, regions, prices)
If app notice that there is no tables - it run updates. 
Each time app.py runs REST API (before it run) - code check if there is postgress.

I did not to use circuitbreakers and backoff python library. 
Usually it is rl good practice in this cases.