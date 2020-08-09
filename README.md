# REST API With Flask & SQL Alchemy

> Todo API using Python Flask, SQL Alchemy with Login Authentication

``` bash
# Create TodoDatabase
$ python
>> from flaskapi import db
>> db.create_all()
>> exit()

# Run Server (http://localhst:5000)
python flaskapi.py
``` 

## Endpoints
* GET     /login    = route for login
* GET     /todo     = route available for all
* GET     /todo/:id  = login required for this route
* POST    /todo   = login required for this route
* PUT     /todo/:id   = login required for this route
* DELETE  /todo/:id   = login required for this route