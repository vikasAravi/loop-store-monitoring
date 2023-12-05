from app.repositories.store import StoreRepository
from app.repositories.store_status import StoreStatusRepository
from app.service.store_status_polling_cron_impl import StoreStatusPollingCronImpl


class StoreStatusPollingCronFactory:

    @staticmethod
    def get_store_status_polling_cron_factory():
        store_repository = StoreRepository()
        store_status_repository = StoreStatusRepository()
        return StoreStatusPollingCronImpl(
            store_repository=store_repository,
            store_status_repository=store_status_repository
        )