import pymongo
from env import srv
def connect():
    # Connect to the database
    connection = pymongo.MongoClient(srv)
    
    # Get a handle to the database
    db = connection.msml
    return db

def insert(data):
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
    db = connect()
    # Get a handle to the posts collection
    # Find all matching documents
    data = db.aqi.find({"city": city, "state": state})
    data = list(data)
    #remove object id
    for d in data:
        d.pop("_id")
    print(data)
    #sort by datetime
    data = sorted(data, key=lambda k: k['datetime'])

    return data