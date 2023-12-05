from app.repositories.store import StoreRepository
from app.service.store_impl import StoreImpl


class StoreFactory:

    @staticmethod
    def get_store_factory():
        store_repository = StoreRepository()
        return StoreImpl(
            store_repository=store_repository
        )