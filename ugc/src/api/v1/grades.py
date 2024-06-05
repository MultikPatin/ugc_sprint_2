from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.grades import GradeModel

routers = Blueprint("grades", __name__, url_prefix=PREFIX_BASE_ROUTE + "/grades")


@routers.route("/", methods=["POST"], strict_slashes=False)
@check_access_token
def create(user: AuthUser):
    request_data = request.json
    request_data["user_id"] = user.id
    try:
        data_model = GradeModel.model_validate(request_data)
        return jsonify(data_model.model_dump()), HTTPStatus.CREATED
    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")

