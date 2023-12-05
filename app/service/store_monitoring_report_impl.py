import datetime

from starlette.responses import FileResponse

from app.clients.queues.kafka_producer import KafkaProducerClientManager
from app.models.store_monitoring_report import StoreMonitoringReportRequest
from app.repositories.store_monitoring_report import StoreMonitoringReportRepository
from app.service.store_monitoring_report import StoreMonitoringReport
from app.utils import get_reports_path

QUEUED = "QUEUED"
IN_PROGRESS = "IN_PROGRESS"
COMPLETED = "COMPLETED"


class StoreMonitoringReportImpl(StoreMonitoringReport):

    def __init__(self, store_monitoring_report_repository: StoreMonitoringReportRepository, kafka_producer:
    KafkaProducerClientManager):
        self.store_monitoring_report_repository = store_monitoring_report_repository
        self.kafka_producer = kafka_producer

    def save_store_monitoring_report_request(self):
        store_monitoring_report_request = StoreMonitoringReportRequest(
            status=QUEUED,
            created_on=datetime.datetime.utcnow(),
            updated_on=datetime.datetime.utcnow(),
            report_path=""
        ).to_dict()
        self.kafka_producer.send_message("store_monitor_topic", "KEY", store_monitoring_report_request)
        return self.store_monitoring_report_repository. \
            save_store_monitoring_report_request(store_monitoring_report_request)

    def get_store_monitoring_report_request(self, request_id):
        _output = self.store_monitoring_report_repository.get_store_monitoring_report_request(request_id)
        if _output["status"] in (QUEUED, IN_PROGRESS):
            return {
                "status": _output["status"]
            }
        file_path = get_reports_path(request_id)
        # Return the file using FileResponse
        return FileResponse(file_path, filename=request_id)
