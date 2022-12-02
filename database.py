'''
    Everything related to database connection
'''
#!/usr/bin/env python

import pymongo
from datetime import datetime
from env import srv


def connect():
    '''
        Connect to the database
    '''

    connection = pymongo.MongoClient(srv)

    # Get a handle to the database
    db = connection.msml
    return db


def insert(data):
    '''
        Insert data into the database
    '''
    db = connect()
    # Get a handle to the posts collection
    collection = db.aqi
    must = ['city', 'state', 'aqi', 'datetime']
    for m in must:
        if m not in data:
            return False, m
    # Insert the data into the collection
    collection.insert_one(data)
    return True, None


def retrieve(city, state):
    '''
        Retrieve data from the database
    '''

    db = connect()
    # Get a handle to the posts collection
    # Find all matching documents
    data = db.aqi.find({"city": city.lower(), "state": state.lower()})
    data = list(data)
    #remove object id
    for d in data:
        d.pop("_id")
    #convert datetime string to datetime object
    for d in data:
        d['datetime'] = datetime.strptime(d['datetime'], '%d/%m/%Y %H:%M:%S')
    #sort by datetime
    data = sorted(data, key=lambda k: k['datetime'])

    #convert datetime object to string
    for d in data:
        d['datetime'] = d['datetime'].strftime("%d/%m/%Y %H:%M:%S")

    return data


def insert_prediction(data):
    '''
        Insert data into the database
    '''
    print(data)
    db = connect()
    # Get a handle to the posts collection
    collection = db.predictions
    # Insert the data into the collection
    #if datetime is already present, update the aqi
    for dictionary in data:
        if collection.find_one({
                "city": dictionary['city'].lower(),
                "state": dictionary['state'].lower(),
                "datetime": dictionary['datetime']
        }):
            collection.update_one(
                {
                    "city": dictionary['city'].lower(),
                    "state": dictionary['state'].lower(),
                    "datetime": dictionary['datetime']
                }, {"$set": {
                    "yhat": dictionary['yhat']
                }})
        else:
            collection.insert_one(dictionary)
    print("inserted")
    return True, None


def retrieve_prediction(city, state):
    '''
        Retrieve data from the database
    '''

    db = connect()
    # Get a handle to the posts collection
    # Find all matching documents
    data = db.predictions.find({"city": city.lower(), "state": state.lower()})
    data = list(data)
    #remove object id
    for d in data:
        d.pop("_id")
    #sort by datetime
    data = sorted(data, key=lambda k: k['datetime'])

    #convert datetime object to string
    for d in data:
        d['datetime'] = d['datetime'].strftime("%d/%m/%Y %H:%M:%S")

    return data