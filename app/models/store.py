import datetime
import uuid
from typing import List

from pydantic import BaseModel, Field


class BusinessHours(BaseModel):
    week_day: int
    start_time: str
    end_time: str


class Store(BaseModel):
    id: str
    name: str
    timezone: str
    business_hours: List[BusinessHours]
    is_online: bool

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "timezone": self.timezone,
            "business_hours": self.business_hours,
            "is_online": self.is_online,
        }
