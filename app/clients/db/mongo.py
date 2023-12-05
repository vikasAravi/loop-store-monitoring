from pymongo import MongoClient


class MongoClusterManager:
    __client = None

    @staticmethod
    def get_instance():
        if MongoClusterManager.__client is None:
            MongoClusterManager()
        return MongoClusterManager.__client

    def __init__(self):
        if MongoClusterManager.__client is not None:
            raise Exception("This class is a singleton")
        else:
            MongoClusterManager.__client = MongoClient(host='mongodb://localhost:27017/')
