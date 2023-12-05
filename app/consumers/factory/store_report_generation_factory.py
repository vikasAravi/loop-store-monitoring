from app.clients.queues.kafka_consumer import KafkaConsumerClientManager
from app.consumers.store_report_generation import StoreReportGenerationConsumer
from app.repositories.store import StoreRepository
from app.repositories.store_monitoring_report import StoreMonitoringReportRepository
from app.repositories.store_status import StoreStatusRepository

import json




class StoreReportGenerationFactory:

    @staticmethod
    def get_store_report_generation_factory():
        store_repository = StoreRepository()
        store_status_repository = StoreStatusRepository()
        store_monitoring_report_repository = StoreMonitoringReportRepository()
        consumer = KafkaConsumerClientManager.get_kafka_consumer("localhost:9093", 'latest',
                                                                 'repost_generation_group', False,
                                                                 lambda m: json.loads(m.decode('utf-8')),
                                                                 100)
        topics = ["store_monitor_topic"]
        consumer.subscribe(topics)

        return StoreReportGenerationConsumer(
            store_repository=store_repository,
            store_status_repository=store_status_repository,
            store_monitoring_report_repository=store_monitoring_report_repository,
            consumer=consumer
        )
