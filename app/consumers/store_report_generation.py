import math

import pandas as pd
import pytz

import logging.config

from app.clients.queues.kafka_consumer import KafkaConsumerClientManager
from app.consumers.consumer import Consumer
from app.repositories.store import StoreRepository
from app.repositories.store_monitoring_report import StoreMonitoringReportRepository
from app.repositories.store_status import StoreStatusRepository
from app.schemas.store_monitoring_report import StoreMetrics
from app.utils import get_reports_path

PAGE_SIZE = 200
REPORT_COLUMNS = ['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week',
                  'downtime_last_hour', 'downtime_last_day', 'downtime_last_week']

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StoreReportGenerationConsumer(Consumer):

    def __init__(self, consumer: KafkaConsumerClientManager, store_repository: StoreRepository,
                 store_status_repository: StoreStatusRepository,
                 store_monitoring_report_repository: StoreMonitoringReportRepository):
        self.consumer = consumer
        self.store_repository = store_repository
        self.store_status_repository = store_status_repository
        self.store_monitoring_report_repository = store_monitoring_report_repository

    def start(self):
        for message in self.consumer.consume_messages():
            request_id = message.value["_id"]
            logger.info(f"STARTED PROCESSING FOR REQUEST ID - {request_id}")
            self.update_store_monitoring_reqeust(message, "IN_PROGRESS")
            self.process_message(request_id)
            self.update_store_monitoring_reqeust(message, "COMPLETED")
            self.consumer.commit_async(message)
            logger.info(f"PROCESSING COMPLETED FOR REQUEST ID - {request_id}")

    def process_message(self, request_id):
        # CREATE A CSV WITH THE HEADERS
        report_df = pd.DataFrame(columns=REPORT_COLUMNS)

        # COUNT THE NUMBER OF STORES FOR PROPER BATCHING & PAGINATION ( AS NUMBER OF STORES CAN BE HUGE )
        number_of_stores = self.store_repository.get_stores_count()

        # CALCULATE THE NUMBER OF PAGES
        number_of_pages = math.ceil(number_of_stores / PAGE_SIZE)

        # FOR EACH PAGE, CALCULATE THE METRICS
        for page in range(1, number_of_pages + 1):
            skip, limit = (page - 1) * PAGE_SIZE, PAGE_SIZE
            store_details = self.store_repository.get_stores(skip, limit)
            store_metrics = self.process_store_metrics(store_details)
            report_df = report_df._append(store_metrics, ignore_index=True)

        # SAVE THE METRICS TO CSV
        file_path = get_reports_path(request_id)
        report_df.to_csv(file_path)

    def process_store_metrics(self, store_details):
        store_ids = [store["_id"] for store in store_details]
        status_details_for_stores = list(self.store_status_repository.get_all_status(store_ids))

        if len(status_details_for_stores) == 0:
            return []

        # CREATE DATA FRAMES
        store_data = pd.DataFrame(store_details)
        status_data = pd.DataFrame(status_details_for_stores)

        # MERGE THE DATA
        # CONVERT UTC TIMESTAMP TO RESPECTIVE STORE TIMEZONE
        merged_data = pd.merge(store_data, status_data, left_on="_id", right_on="store_id")
        merged_data['timestamp'] = pd.to_datetime(merged_data['created_on'])
        merged_data['timestamp_utc'] = merged_data['timestamp'].dt.tz_localize('UTC')
        merged_data['timestamp_local'] = merged_data.apply(
            lambda row: row['timestamp_utc'].tz_convert(pytz.timezone(row['timezone'])),
            axis=1
        )

        # CALCULATE THE METRICS
        metrics = []
        for store_id in store_ids:

            # GET THE DATA FOR SPECIFIC STORE
            store_information = merged_data[merged_data["store_id"] == store_id]

            # CREATE A NEW COLUMN FOR BUSINESS HOURS CHECKS
            store_information['timestamp_local_datetime'] = pd.to_datetime(store_information['timestamp_local'])

            # APPLY THE RULE AND REMOVE THE ROWS WHICH ARE NOT IN BUSINESS HOURS
            store_information['is_within_business_hours'] = store_information.apply(self.is_within_business_hours,
                                                                                    axis=1)

            # IF THE METRICS ARE NOT FOUND, CONTINUE WITH THE DEFAULT RESPONSE
            if len(store_information.index) == 0:
                metrics.append(StoreMetrics(
                    store_id=store_id,
                    uptime_last_hour=0,
                    uptime_last_week=0,
                    uptime_last_day=0,
                    downtime_last_hour=0,
                    downtime_last_week=0,
                    downtime_last_day=0
                ).to_dict())
                continue

            # SET THE INDEX AND GET THE TIMEZONE
            # GET THE CURRENT TIMESTAMP IN THE TIMEZONE
            store_information.set_index('timestamp_local_datetime', inplace=True)
            store_timezone = store_information['timezone'].iloc[0]
            now_store_tz = pd.to_datetime('now', utc=True).tz_convert(pytz.timezone(store_timezone))

            # SAMPLING OF ONE HOUR ( FOR ALL THE HOURS IN A DAY FOR THE INDEX )
            store_information_resampled = store_information.resample('1H').first()

            # LINEAR INTERPOLATION FOR THE IS_WITHIN_BUSINESS_HOURS
            store_information_resampled['is_within_business_hours'] = \
                store_information_resampled['is_within_business_hours'].interpolate(method='linear').astype(bool)

            # CONVERSIONS OF THE STATUS TO BOOL TYPE ( active as TRUE and inactive as FALSE )
            store_information_resampled['status'] = store_information_resampled['status'].map(
                {'active': True, 'inactive': False})
            store_information_resampled['status'] = store_information_resampled['status'].interpolate(
                method='linear').astype(bool)

            # FILTER OUT THE STORE SAMPLES WHERE OUT OF BUSINESS HOURS
            store_information_resampled = store_information_resampled[
                store_information_resampled["is_within_business_hours"]]

            # CALCULATE THE STORE METRICS AND APPEND TO RESULT SET
            store_metrics = self.get_store_metrics(store_id, store_information_resampled, now_store_tz)
            metrics.append(store_metrics)

        return metrics

    def update_store_monitoring_reqeust(self, message, status):
        filter_query = {
            "_id": message.value['_id'],
        }
        update_query = {
            "$set": {
                "status": status
            }
        }
        self.store_monitoring_report_repository. \
            update_store_monitoring_request(filter_query, update_query)

    def get_store_metrics(self, store_id, store_information_resampled, now_store_tz):

        # BASIS ON THE TIMESTAMP(LOCAL) SPLIT THE DATA INTO LAST WEEK, LAST DAY and LAST HOUR
        last_week_data = self.get_last_week_data(store_information_resampled, now_store_tz)
        last_day_data = self.get_last_day_data(store_information_resampled, now_store_tz)
        last_hour_data = self.get_last_hour_data(store_information_resampled, now_store_tz)

        # UPTIME & DOWNTIME BASIS ON THE STATUS FOR LAST HOUR
        uptime_last_hour = last_hour_data['status'].eq(True).sum()
        downtime_last_hour = last_hour_data['status'].eq(False).sum()

        # UPTIME & DOWNTIME BASIS ON THE STATUS FOR LAST DAY
        uptime_last_day = last_day_data['status'].eq(True).sum()
        downtime_last_day = last_day_data['status'].eq(False).sum()

        # UPTIME & DOWNTIME BASIS ON THE STATUS FOR LAST WEEK
        uptime_last_week = last_week_data['status'].eq(True).sum()
        downtime_last_week = last_week_data['status'].eq(False).sum()

        # CONVERTING METRICS TO DESIRED UNITS
        uptime_last_hour_minutes = uptime_last_hour * 60
        downtime_last_hour_minutes = downtime_last_hour * 60
        uptime_last_day_hours = math.ceil(uptime_last_day / 60)
        downtime_last_day_hours = math.ceil(downtime_last_day / 60)
        uptime_last_week_hours = math.ceil(uptime_last_week / 60)
        downtime_last_week_hours = math.ceil(downtime_last_week / 60)

        return StoreMetrics(
            store_id=store_id,
            uptime_last_hour=uptime_last_hour_minutes,
            uptime_last_week=uptime_last_week_hours,
            uptime_last_day=uptime_last_day_hours,
            downtime_last_hour=downtime_last_hour_minutes,
            downtime_last_week=downtime_last_week_hours,
            downtime_last_day=downtime_last_day_hours
        ).to_dict()

    def get_last_week_data(self, store_information, now_store_tz):
        return store_information[
            (store_information.index >= now_store_tz - pd.DateOffset(weeks=1)) &
            (store_information.index < now_store_tz - pd.Timedelta(days=1))
            ]

    def get_last_day_data(self, store_information, now_store_tz):
        return store_information[
            (store_information.index >= now_store_tz - pd.Timedelta(days=1)) &
            (store_information.index < now_store_tz - pd.Timedelta(hours=1))
            ]

    def get_last_hour_data(self, store_information, now_store_tz):
        return store_information[
            (store_information.index >= now_store_tz - pd.Timedelta(hours=1)) &
            (store_information.index < now_store_tz - pd.Timedelta(minutes=1))
            ]

    def is_within_business_hours(self, row):
        week_day = row["timestamp_local_datetime"].weekday()
        business_hours = next((item for item in row['business_hours'] if item['week_day'] == week_day), None)
        if business_hours:
            start_time = pd.to_datetime(business_hours["start_time"]).time()
            end_time = pd.to_datetime(business_hours["end_time"]).time()
            return start_time <= row["timestamp_local_datetime"].time() <= end_time
        return True
