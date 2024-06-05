from typing import Annotated

from fast_depends import Depends, inject
from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException

from src.api.v1.events import routers as event_routers
from src.api.v1.grades import routers as grade_routers
from src.brokers.init import KafkaInit, get_kafka_init
from src.core.config import settings

swagger_blueprint = get_swaggerui_blueprint(
    settings.swagger.docs_url,
    settings.swagger.api_url,
    config={
        "app_name": settings.swagger.project_name,
    },
)


@inject
def init_kafka(kafka_init_app: Annotated[KafkaInit, Depends(get_kafka_init)]):
    kafka_init_app.create_topics()


def create_app():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(swagger_blueprint)
    flask_app.register_blueprint(event_routers)
    flask_app.register_blueprint(grade_routers)

    init_kafka()  # type:ignore

    return flask_app


app = create_app()


@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code
