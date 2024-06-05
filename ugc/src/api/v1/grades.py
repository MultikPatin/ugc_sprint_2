from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.grades import Grade

routers = Blueprint("grades", __name__, url_prefix=PREFIX_BASE_ROUTE + "/grades")


@routers.route("/", methods=["POST"], strict_slashes=False)
@check_access_token
def create(user: AuthUser):
    request_data = request.json
    try:
        collection_model = Grade.model_validate(request_data)
        collection_model.user_id = user.id
        return jsonify(collection_model.model_dump()), HTTPStatus.CREATED
    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")
