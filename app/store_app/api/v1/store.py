from fastapi import APIRouter

from app.schemas.store import StoreRequest
from app.service.store_factory import StoreFactory

router = APIRouter()

store_factory = StoreFactory.get_store_factory()


@router.post("/")
def create_store(store: StoreRequest):
    response = store_factory.save_store(store.to_dict())
    return response

