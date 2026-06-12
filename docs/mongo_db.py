from pymongo import MongoClient

def get_collection():

    client = MongoClient(
        "mongodb://mongodb:27017/"
    )

    db = client["telemetry"]

    return db["raw_data"]
