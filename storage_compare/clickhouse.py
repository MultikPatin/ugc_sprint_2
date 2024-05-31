from clickhouse_connect.driver.httpclient import HttpClient


class ClickhouseManager:
    """
    Класс для взаимодействия для Clickhouse
    """
    def __init__(self, client: HttpClient) -> None:
        self.client = client

    def create_initial_table(self):
        """
        Создает талицу по-умолчанию для проведения тестов
        """

        self.client.command('''
            CREATE TABLE IF NOT EXISTS  default.events_test
                (
                `service` String,
                `user` UUID,
                `timestamp` DateTime,
                `entity_type` String,
                `entity` String,
                `action` String
                )
                ENGINE = MergeTree
                ORDER BY (service, user, timestamp, entity_type, entity, action)
                SETTINGS index_granularity = 8192
        ''')

    def insert_data(self, data: list[list]) -> None:
        """
        Метод для вставки данных в тестовую таблицу
        """
        self.client.insert('default.events_test', data,
                           column_names=['service', 'user', 'timestamp', 'entity_type', 'entity', 'action'])
