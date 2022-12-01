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