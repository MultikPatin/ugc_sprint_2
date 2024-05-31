import datetime
import clickhouse_connect
from faker import Faker

from uuid import uuid4

from clickhouse import ClickhouseManager
from config import settings

fake = Faker()

BATCH_COUNT = 10000
BATCH_SIZE = 100


with clickhouse_connect.get_client(host=settings.clickhouse.host, username=settings.clickhouse.username,
                                   password=settings.clickhouse.password) as client:
    manager = ClickhouseManager(client)
    manager.create_initial_table()

    start: datetime.datetime = datetime.datetime.now()

    for _ in range(BATCH_COUNT):
        try:
            rows = []
            for _ in range(BATCH_SIZE):
                row = [
                    fake.name(),
                    uuid4(),
                    fake.date_time(),
                    fake.name(),
                    fake.name(),
                    fake.name()

                ]
                rows.append(row)
            manager.insert_data(rows)
        except Exception:
            continue

    total_time: datetime.timedelta = datetime.datetime.now() - start
    print(f"Total time: {total_time}")

