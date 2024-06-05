import time
from contextlib import contextmanager
from functools import wraps

import psycopg2
from psycopg2.extensions import connection as _connection

from config import settings


def timeit(func):
    """
    Декоратор для измерения время работы функции
    """

    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Время выполнения: {total_time:.6f} секунд')
        return result

    return timeit_wrapper


@contextmanager  # type: ignore
def conn_context_postgres(dsl: dict) -> _connection:  # type: ignore
    """
    Контекстый менеджер, осблуживаний соединения к Postgres
    """
    conn: _connection = psycopg2.connect(**dsl)
    yield conn
    conn.close()


def get_postgres_dsl() -> dict:
    """
    Создает и возвращает  подключения к БД postgres
    """

    return {'dbname': settings.postgres.db,
            'user': settings.postgres.username,
            'password': settings.postgres.password,
            'host': settings.postgres.host,
            'port': settings.postgres.port}
