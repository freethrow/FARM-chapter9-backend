# a function that returns a sample of N cars
from pymongo import MongoClient
from decouple import config


# connect to mongodb
DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)

client = MongoClient(DB_URL)
db = client[DB_NAME]
cars = db["cars"]


def make_query(cars_number):

    query = [
        {"$match": {"year": {"$gt": 2010}}},
        {
            "$project": {
                "_id": 0,
                "km": 1,
                "year": 1,
                "make": 1,
                "price": 1,
                "cm3": 1,
                "brand": 1,
            }
        },
        {"$sample": {"size": cars_number}},
        {"$sort": {"brand": 1, "make": 1, "year": 1}},
    ]

    full_query = cars.aggregate(query)
    return [el for el in full_query]
