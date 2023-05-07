from pymongo import MongoClient

from mongodb_api_config import mongo_api_address, mongo_database_name


class MongoApiService:
    """
    Object that handles communication with mongodb
    """

    def __init__(self):
        """
        Connect to MongoDB database
        """
        self.client = MongoClient(mongo_api_address)
        self.db = self.client[mongo_database_name]


mongo_api_service = MongoApiService()
