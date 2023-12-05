import datetime
from typing import List

from pydantic import BaseModel


class BusinessHoursSchema(BaseModel):
    week_day: int
    start_time: str
    end_time: str

    def to_dict(self):
        return {
            "week_day": self.week_day,
            "start_time": self.start_time,
            "end_time": self.end_time
        }


class StoreRequest(BaseModel):
    id: str
    name: str
    timezone: str
    is_online: bool
    business_hours: List[BusinessHoursSchema]

    def to_dict(self):
        return {
            "_id": self.id,
            "name": self.name,
            "timezone": self.timezone,
            "is_online": self.is_online,
            "business_hours": [business_hour.to_dict() for business_hour in self.business_hours if len(self.business_hours) > 0]
        }
