import csv
from datetime import datetime

from app.models.store import Store, BusinessHours
from app.repositories.store import StoreRepository

STORE_TIMEZONE_FILE_PATH = "/Users/vikash/Downloads/bq-results-20230125-202210-1674678181880.csv"
STORE_BUSINESS_HOURS_FILE_PATH = "/Users/vikash/Downloads/Menu hours.csv"

store_repository = StoreRepository()

if __name__ == "__main__":
    file = open(STORE_TIMEZONE_FILE_PATH)
    csv_reader = csv.reader(file)
    headers = next(csv_reader)

    store_records = []
    for row in csv_reader:
        print(row)
        store_records.append(Store(
            id=row[0],
            name=row[0],
            timezone=row[1],
            is_online=True,
            business_hours=[]
        ).to_dict())

    store_repository.bulk_save(store_records)

    # BUSINESS HOURS

    file = open(STORE_BUSINESS_HOURS_FILE_PATH)
    csv_reader = csv.reader(file)
    headers = next(csv_reader)

    for row in csv_reader:
        print(row)
        business_hour = {
            "week_day":row[1],
            "start_time":row[2],
            "end_time":row[3]
        }
        store_repository.update_business_hours(row[0], business_hour)



