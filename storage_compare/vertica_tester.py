import datetime
import multiprocessing
import os
import vertica_python
from faker import Faker
from uuid import uuid4

from config import settings
from vertica import VerticaManager

fake = Faker()

BATCH_COUNT = 100
BATCH_SIZE = 10000
proc_count = os.cpu_count()


connection_info: dict = {
    'host': settings.vertica.host,
    'port': settings.vertica.port,
    'user': settings.vertica.user,
    'password': settings.vertica.password,
    'database': settings.vertica.database,
    'autocommit': True
}


def insert_test_data(conn_info, batch_size, batch_count) -> None:
    with vertica_python.connect(**conn_info) as vertica_connection:
        vertica_manager = VerticaManager(vertica_connection)

        for _ in range(batch_count):
            rows = []
            for _ in range(batch_size):
                row = [
                    fake.name(),
                    uuid4(),
                    fake.date_time(),
                    fake.name(),
                    fake.name(),
                    fake.name()

                ]
                rows.append(row)
            vertica_manager.insert_data(rows)


if __name__ == '__main__':
    with vertica_python.connect(**connection_info) as connection:
        manager = VerticaManager(connection)
        manager.create_initial_table()
    processes = []
    for _ in range(proc_count):
        processes.append(
            multiprocessing.Process(target=insert_test_data, args=(connection_info, BATCH_SIZE, BATCH_COUNT)))
    start = datetime.datetime.now()
    [p.start() for p in processes]
    [p.join() for p in processes]

    total_time = datetime.datetime.now() - start
    print(f"Total time: {total_time}")
