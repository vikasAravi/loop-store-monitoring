from fastapi import APIRouter
import logging.config

from app.service.store_service_factory import StoreMonitoringReportFactory


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

store_monitoring_report_factory = StoreMonitoringReportFactory.get_store_monitoring_report_service()


@router.post("/trigger_report")
def trigger_report():
    response = store_monitoring_report_factory.save_store_monitoring_report_request()
    logger.info(f"TRIGGER REPORT RESPONSE - {response}")
    return response


@router.get("/fetch_report/{request_id}")
def get_report(request_id: str):
    response = store_monitoring_report_factory.get_store_monitoring_report_request(request_id)
    logger.info(f"FETCH REPORT RESPONSE FOR REQUEST ID {request_id} - {response}")
    return response

