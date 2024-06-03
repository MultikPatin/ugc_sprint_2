from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from src.api.v1.events import routers as event_routers
from src.core.config import settings
from src.core.init import KafkaInit, get_kafka_init

swagger_blueprint = get_swaggerui_blueprint(
    settings.swagger.docs_url,
    settings.swagger.api_url,
    config={
        "app_name": settings.swagger.project_name,
    },
)


def init_kafka(kafka_init_app: KafkaInit = get_kafka_init()):
    kafka_init_app.create_topics()


def create_app():
    flask_app = Flask(__name__)
    flask_app.register_blueprint(swagger_blueprint)
    flask_app.register_blueprint(event_routers)

    init_kafka()

    return flask_app


app = create_app()
