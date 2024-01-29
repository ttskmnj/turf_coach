# turf manager

## Prerequisites
- docker-compose
- crontab

## How to run
### 1. create `.env` file
create `.env` file in root of this repository
```
$ touch .env
```
and fill following informations
```
MONGO_INITDB_ROOT_USERNAME=<MONGODB USER> 
MONGO_INITDB_ROOT_PASSWORD=<MONGODB PASSWORD>
MONGO_INITDB_DATABASE=<MONGODB DATABESE>
MONGO_URL=mongodb://<MONGODB USER>:<MONGODB PASSWORD>@mongo:27017

OPENWETHERMAP_URL=http://api.openweathermap.org/
OPENWETHERMAP_KEY=<OPENWETHERMAP APIKEY>
```

### 2. start containers
run following command in root of this repository
```
$ docker-compose up -d
```

### set cron job
set cron job to call `http://0.0.0.0:8000/pitch/update_next_maintenance/` every day at 10:00:00

following command will open editor. 
```
crontab -e
```

add following line and save it.
```
0 10 * * * curl http://0.0.0.0:8000/pitch/update_next_maintenance/ >> /tmp/cronerr.log
```

### stop containers
if you want to stop containers run following command in root of this repository
```
$ docker-compose down
```

## Endpoints

### Create pitch
#### request
```
POST http://0.0.0.0:8000/pitch/
# body
{
    "name":"Pitch1",
    "city":"Leipzig",
    "state":"Saxony",
    "country":"DE",
    "type":1,
    "last_maintenace_date":"2022-05-15T06:54:36",
    "next_maintenace_date":"2025-02-15T06:53:16",
    "condition":2
}
```

### Get all Pitches
#### request
```
GET http://0.0.0.0:8000/pitch/
```

#### response
```
[
    {
        "_id": "65b4ee2a27dfa5c4abc6b540",
        "name": "Pitch1",
        "city": "Leipzig",
        "state": "Saxony",
        "country": "DE",
        "type": 1,
        "last_maintenace_date": "2022-05-15T06:54:36",
        "next_maintenace_date": "2024-01-30T11:51:17.183000",
        "condition": 2
    }
]
```

### Get one Pitch
#### request
```
GET http://0.0.0.0:8000/pitch/<PITCH ID>
```

#### response
```
{
    "_id": "65b4ee2a27dfa5c4abc6b540",
    "name": "Pitch1",
    "city": "Leipzig",
    "state": "Saxony",
    "country": "DE",
    "type": 1,
    "last_maintenace_date": "2022-05-15T06:54:36",
    "next_maintenace_date": "2024-01-30T11:51:17.183000",
    "condition": 2
}
```

### Update next maintenance date
#### request
```
GET http://0.0.0.0:8000/pitch/update_next_maintenance/
```

#### response
```
{'msg': "update next maintenance"}
```

### Get pitch need maintenance in 3days
#### request
```
GET http://0.0.0.0:8000/pitch/need_maintenance/
```

#### response
```
[
    {
        "_id": "65b4ee2a27dfa5c4abc6b540",
        "name": "Pitch1",
        "city": "Leipzig",
        "state": "Saxony",
        "country": "DE",
        "type": 1,
        "last_maintenace_date": "2022-05-15T06:54:36",
        "next_maintenace_date": "2024-01-30T11:51:17.183000",
        "condition": 2
    }
]
```

### update pitch
#### request
```
PUT http://0.0.0.0:8000/pitch/
# body
{
"name":"str2",
"type":1,
"last_maintenace_date":"1979-05-15T06:54:36",
"next_maintenace_date":"2025-02-15T06:53:16",
"condition":2
}
```

#### response
```
{'msg':  "pitch: <PITCH ID> is updated"}
```

## delete pitch
#### request
```
DELETE http://0.0.0.0:8000/pitch/
```

#### response
```
{"message": "pitch: <PITCH ID> is deleted"}
```
