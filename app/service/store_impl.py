from app.repositories.store import StoreRepository
from app.service.store import Store


class StoreImpl(Store):

    def __init__(self, store_repository: StoreRepository):
        self.store_repository = store_repository

    def get_store(self, store_id):
        _output = self.store_repository.get_store(store_id)
        return _output

    def save_store(self, store):
        _output = self.store_repository.save_store(store)
        return _output
