from app.clients.queues.kafka_producer import KafkaProducerClientManager
from app.repositories.store_monitoring_report import StoreMonitoringReportRepository
from app.service.store_monitoring_report_impl import StoreMonitoringReportImpl


class StoreMonitoringReportFactory:

    @staticmethod
    def get_store_monitoring_report_service():
        store_monitoring_report_repository = StoreMonitoringReportRepository()
        kafka_producer = KafkaProducerClientManager.get_kafka_producer()
        return StoreMonitoringReportImpl(store_monitoring_report_repository, kafka_producer)
