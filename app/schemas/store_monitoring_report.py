from pydantic import BaseModel


class StoreMetrics(BaseModel):
    store_id: str
    uptime_last_hour: int
    uptime_last_day: int
    uptime_last_week: int
    downtime_last_hour: int
    downtime_last_day: int
    downtime_last_week: int

    def to_dict(self):
        return {
            "store_id": self.store_id,
            "uptime_last_hour": self.uptime_last_hour,
            "uptime_last_day": self.uptime_last_day,
            "uptime_last_week": self.uptime_last_week,
            "downtime_last_hour": self.downtime_last_hour,
            "downtime_last_day": self.downtime_last_day,
            "downtime_last_week": self.downtime_last_week
        }
