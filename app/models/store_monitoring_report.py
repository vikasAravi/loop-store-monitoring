import datetime
import uuid

from pydantic import BaseModel, Field


class StoreMonitoringReportRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    created_on: datetime.datetime
    updated_on: datetime.datetime
    status: str
    report_path: str

    def to_dict(self):
        return {
            "_id": self.id,
            "created_on": str(self.created_on),
            "updated_on": str(self.updated_on),
            "status": self.status,
            "report_path": self.report_path
        }


