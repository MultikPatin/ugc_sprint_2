from vertica_python.vertica.connection import Connection


class VerticaManager:
    """
    Класс для взаимодействия с Vertica
    """

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
        self.cursor = connection.cursor()

    def create_initial_table(self) -> None:
        """
        Создает талицу по-умолчанию для проведения тестов
        """

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS  events_test
                (
                service VARCHAR(256) NOT NULL,
                user_uuid VARCHAR(256) NOT NULL,
                timestamp DATETIME NOT NULL,
                entity_type VARCHAR(256) NOT NULL,
                entity VARCHAR(256) NOT NULL,
                action VARCHAR(256) NOT NULL
                )

        """)

    def insert_data(self, data: list[list]) -> None:
        self.cursor.executemany(
            "INSERT INTO events_test(service, user_uuid, timestamp, entity_type, entity, action) VALUES (?,?,?,?,?,?)",
            data, use_prepared_statements=True)
