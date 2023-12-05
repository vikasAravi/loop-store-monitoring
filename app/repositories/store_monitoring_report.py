from app.clients.db.mongo import MongoClusterManager

mongo_client = MongoClusterManager.get_instance()
db_cluster = mongo_client["store"]
store_monitoring_reports_collection = db_cluster["storeMonitoringReports"]


class StoreMonitoringReportRepository:

    def save_store_monitoring_report_request(self, store_monitoring_report_request):
        try:
            _output = store_monitoring_reports_collection.insert_one(store_monitoring_report_request)
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


    def get_store_monitoring_report_request(self, request_id):
        query = {
            "_id": request_id
        }
        _output = store_monitoring_reports_collection.find_one(query)
        return _output

    def update_store_monitoring_request(self, filter_query, update_query):
        _output = store_monitoring_reports_collection.update_one(filter_query, update_query)
        return _output

