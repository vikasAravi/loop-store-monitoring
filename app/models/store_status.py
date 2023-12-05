import datetime
import uuid

from pydantic import BaseModel, Field


class StoreStatus(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    store_id: str
    status: str
    created_on: datetime.datetime

    def to_dict(self):
        return {
            "_id": self.id,
            "created_on": str(self.created_on),
            "store_id": self.store_id,
            "status": self.status,
        }
