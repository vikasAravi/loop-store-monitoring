from app.clients.db.mongo import MongoClusterManager

mongo_client = MongoClusterManager.get_instance()
db_cluster = mongo_client["store"]
store_status_collection = db_cluster["store_status"]

class StoreStatusRepository():

    def save_store_status(self, store_status):
        try:
            _output = store_status_collection.insert_one(store_status)
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
                "error_message": "The request can't be submitted " + str(e)
            }

    def get_all_status(self, store_ids):
        filter_query = {
            "store_id": {"$in": store_ids}
        }
        _output = store_status_collection.find(filter_query)
        return _output

    def bulk_save(self, store_status):
        _output = store_status_collection.insert_many(store_status)
        return _output


