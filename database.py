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
    updated = 0
    inserted = 0
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
            updated += 1

        else:
            collection.insert_one(dictionary)
            inserted += 1
    print(f"inserted: {inserted}, updated: {updated}")
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

    #convert datetime string to datetime object
    for d in data:
        if isinstance(d['datetime'], str):
            d['datetime'] = datetime.strptime(d['datetime'],
                                              '%d/%m/%Y %H:%M:%S')
    #sort by datetime
    data = sorted(data, key=lambda k: k['datetime'])

    #convert datetime object to string
    for d in data:
        d['datetime'] = d['datetime'].strftime("%d/%m/%Y %H:%M:%S")

    return data


def delete():
    #delete all the data where date is greater than 09/12/2022 21:00:00
    db = connect()
    # Get a handle to the posts collection
    collection = db.predictions
    collection.delete_many({"datetime": {"$gt": "09/12/2022 21:00:00"}})


import json


def download_as_json(city, state):
    '''
        Download data as json
    '''
    filename = f"{city}_{state}.json"
    #get prediction data
    data = retrieve_prediction(city, state)
    with open(filename, 'w') as f:
        json.dump(data, f)


import pandas as pd


def json_to_df(filename):
    '''
        Convert json to dataframe
    '''
    with open(filename, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    #convert datetime string to datetime object
    df['datetime'] = pd.to_datetime(df['datetime'], format="%d/%m/%Y %H:%M:%S")
    #delete data where date is greater than 09/12/2022 21:00:00
    compare_date = pd.to_datetime("09/12/2022 21:00:00",
                                  format="%d/%m/%Y %H:%M:%S")

    df = df[df['datetime'] < compare_date]
    #convert datetime object to string
    df['datetime'] = df['datetime'].dt.strftime("%d/%m/%Y %H:%M:%S")
    #save to json
    df.to_json(f"{filename.replace('.json', '_new.json')}", orient='records')
    return df


def delete_all():
    db = connect()
    # Get a handle to the posts collection
    collection = db.predictions
    collection.delete_many({})


def insert_from_json(filename):
    '''
        Insert data from json
    '''
    df = json_to_df(filename)
    data = df.to_dict('records')
    insert_prediction(data)
