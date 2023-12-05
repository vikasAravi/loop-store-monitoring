import csv
import uuid
from datetime import datetime

from app.models.store_status import StoreStatus
from app.repositories.store_status import StoreStatusRepository

STORE_STATUS_FILE_PATH = "/Users/vikash/Downloads/store status.csv"

store_status_repository = StoreStatusRepository()

if __name__ == "__main__":
    file = open(STORE_STATUS_FILE_PATH)
    csv_reader = csv.reader(file)
    headers = next(csv_reader)

    store_status_records = []
    for row in csv_reader:
        print(row)
        store_status_records.append(StoreStatus(
            id = uuid.uuid4(),
            created_on=datetime.utcnow(),
            store_id=row[0],
            status=row[1],
            timezone=row[2],

        ).to_dict())

    store_status_repository.bulk_save(store_status_records)



