import datetime
import math
import uuid

import logging.config

from app.models.store_status import StoreStatus
from app.repositories.store import StoreRepository
from app.repositories.store_status import StoreStatusRepository
from app.service.store_status_polling_cron import StoreStatusPollingCron
from app.coro import event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


PAGE_SIZE = 500


class StoreStatusPollingCronImpl(StoreStatusPollingCron):

    def __init__(self, store_repository: StoreRepository, store_status_repository: StoreStatusRepository):
        self.store_repository = store_repository
        self.store_status_repository = store_status_repository

    def init_store_status_poll(self):
        logger.info("INIT THE STORE STATUS POLL")

        number_of_documents = self.store_repository.get_stores_count()
        if number_of_documents > 0:
            batches = math.ceil(number_of_documents / PAGE_SIZE)
            for batch in range(0, batches):
                event.fire_and_forgot(self.poll_store_status_in_batches(batch + 1))
        else:
            logger.info("NO STORES AVAILABLE TO REFRESH")

        logger.info("STORE STATUS POLL JOB COMPLETED")

    async def poll_store_status_in_batches(self, page_number):
        skip = (page_number - 1) * PAGE_SIZE
        store_details = self.store_repository.get_stores(skip, PAGE_SIZE)
        if store_details is not None and len(store_details) > 0:
            for store in store_details:
                store_status = StoreStatus(
                    id=uuid.uuid4(),
                    store_id=store["_id"],
                    status="active" if store["is_online"] else "inactive",
                    created_on=datetime.datetime.utcnow()
                ).to_dict()
                self.store_status_repository.save_store_status(store_status)