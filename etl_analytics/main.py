import logging
import time
import sentry_sdk

from src.utils.logger import create_logger
from src.config import settings

content_name = settings.kafka.topic

match content_name:
    case "events":
        from src.services.events import KafkaExtractor, ClickHouseLoader
    case "favorites":
        from src.services.favorites import KafkaExtractor, ClickHouseLoader  # type: ignore
    case "grades":
        from src.services.grades import KafkaExtractor, ClickHouseLoader  # type: ignore
    case "reviews":
        from src.services.reviews import KafkaExtractor, ClickHouseLoader  # type: ignore
    case _:
        raise ValueError(f"Unknown content name: {content_name}")


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
    sentry_sdk.init(
        dsn=settings.sentry.dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
    logger = create_logger(f"ETL analytics {content_name.upper()}")
    with (
        KafkaExtractor(settings.kafka) as kafka,
        ClickHouseLoader(settings.clickHouse) as clickhouse,
    ):
        logger.info(f"START ETL analytics {content_name.upper()}")
        etl(logger, kafka, clickhouse)
