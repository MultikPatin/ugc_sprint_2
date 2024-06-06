from http import HTTPStatus

from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.db.collections import Grade
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.grades import GradeModel

routers = Blueprint("grades", __name__, url_prefix=PREFIX_BASE_ROUTE + "/grades")


@routers.route("/", methods=["POST"], strict_slashes=False)
@check_access_token
async def create(user: AuthUser):
    request_data = request.json
    try:
        data_model = GradeModel.model_validate(request_data)
        data_model.user_id = user.id
        grade = Grade(
            film_id="cf083ea9-aa9f-4dd0-b8ee-29393c1a0a31",
            rating=10,
            user_id="bf051197-081c-42ae-9ef3-566f49d58a73"
        )
        await grade.create()
        return jsonify(grade.model_dump()), HTTPStatus.CREATED
    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")
