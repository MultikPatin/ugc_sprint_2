import logging
from typing import Annotated

import logstash
from fast_depends import Depends, inject
from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException

from src.api.v1.events import routers as event_routers
from src.api.v1.favorites import routers as favorite_routers
from src.api.v1.grades import routers as grade_routers
from src.api.v1.reviews import routers as review_routers
from src.brokers.kafka_init import KafkaInit, get_kafka_init
from src.core.config import settings
from src.db.mongo import MongoDBInit, get_mongodb_init

swagger_blueprint = get_swaggerui_blueprint(
    settings.swagger.docs_url,
    settings.swagger.api_url,
    config={
        "app_name": settings.swagger.project_name,
    },
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

logstash_handler = logstash.LogstashHandler(
    settings.logstash.logstash_host, settings.logstash.logstash_port, version=1, tags=["ugc"]
)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get("X-Request-Id")
        return True


@inject
def init_kafka(kafka_init_app: Annotated[KafkaInit, Depends(get_kafka_init)]):
    kafka_init_app.create_topics()


@inject
def init_mongodb(mongodb_init_app: Annotated[MongoDBInit, Depends(get_mongodb_init)]):
    mongodb_init_app.create_collections()


def create_app():
    flask_app = Flask(__name__)

    init_mongodb()  # type:ignore

    flask_app.register_blueprint(swagger_blueprint)
    flask_app.register_blueprint(event_routers)
    flask_app.register_blueprint(grade_routers)
    flask_app.register_blueprint(favorite_routers)
    flask_app.register_blueprint(review_routers)

    init_kafka()  # type:ignore

    return flask_app


app = create_app()

app.logger.addFilter(RequestIdFilter())
app.logger.addHandler(logstash_handler)


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code
