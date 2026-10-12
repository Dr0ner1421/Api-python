import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(
    os.getenv("MONGODB_URI", "mongodb://localhost:27017"),
    serverSelectionTimeoutMS=5000,
)
database = client[os.getenv("MONGODB_DATABASE", "proyecto")]


def get_collection(name: str):
    return database[name]
