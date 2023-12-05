from app.clients.db.mongo import MongoClusterManager

mongo_client = MongoClusterManager.get_instance()
db_cluster = mongo_client["store"]
stores_collection = db_cluster["stores"]


class StoreRepository:

    def get_stores_count(self):
        _output = stores_collection.count_documents({})
        return _output

    def get_stores(self, skip, limit):
        _output = list(stores_collection.find().skip(skip).limit(limit))
        return _output

    def get_store(self, store_id):
        filter_query = {
            "_id": store_id
        }
        _output = stores_collection.find_one(filter_query)
        return _output

    def save_store(self, store):
        try:
            _output = stores_collection.insert_one(store)
            if _output.inserted_id:
                return {
                    "request_id": str(_output.inserted_id),
                    "success_message": "The request has submitted successfully"
                }
            else:
                return {
                    "error_message": "The request can't be submitted"
                }
        except Exception as e:
            return {
                "error_message": "error while saving the store - " + str(e)
            }

    def bulk_save(self, stores):
        _output = stores_collection.insert_many(stores)
        return _output

    def update_business_hours(self, store_id, business_hour):
        filter = {"_id": store_id}
        update = {"$push": {"business_hours": business_hour}}
        _output = stores_collection.update_one(filter, update)
        return _output
