from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.events import EventModel
from src.services.handlers import get_event_handler

routers = Blueprint("events", __name__, url_prefix=PREFIX_BASE_ROUTE + "/events")

event_handler = get_event_handler()


@routers.errorhandler(HTTPStatus.BAD_REQUEST)
def resource_not_found(event):
    return jsonify(error=str(event)), HTTPStatus.BAD_REQUEST


@routers.errorhandler(HTTPStatus.FORBIDDEN)
def resource_forbidden(event):
    return jsonify(error=str(event)), HTTPStatus.FORBIDDEN


@routers.route("/", methods=["POST"], strict_slashes=False)
@check_access_token
def events(user: AuthUser):
    key_event = request.args.get("key")
    request_data = request.json

    if key_event is None:
        abort(
            HTTPStatus.BAD_REQUEST,
            description="Missing required parameter `key`",
        )

    try:
        data_model = EventModel.model_validate(request_data)
        data_model.user = user.id
        event_handler.send_message(topic="events", key=key_event, data=data_model)
    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")

    return jsonify({"message": "Message sent"}), HTTPStatus.ACCEPTED
