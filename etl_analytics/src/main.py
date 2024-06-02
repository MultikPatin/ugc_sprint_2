import logging
import time

from src.utils.logger import create_logger
from src.config import settings
from src.helpers.extractor import KafkaExtractor
from src.helpers.loader import ClickHouseLoader


def etl(
    logger: logging.Logger,
    extractor: KafkaExtractor,
    loader: ClickHouseLoader,
) -> None:
    messages = []
    last_received_time = time.time()

    while True:
        for message in extractor.get_data():
            messages.append(message)
            if (
                len(messages) >= settings.kafka.batch_size
                or (time.time() - last_received_time) >= settings.app.sleep_time
            ):
                loader.write_data(messages)
                extractor.commit()
                messages.clear()
                last_received_time = time.time()
                logger.info("recorded %s messages in clickhouse", len(messages))


if __name__ == "__main__":
    logger = create_logger("ETL analytics Main")
    with (
        KafkaExtractor(settings.kafka) as kafka,
        ClickHouseLoader(settings.clickHouse) as clickhouse,
    ):
        logger.info("START ETL analytics Main")
        etl(logger, kafka, clickhouse)
