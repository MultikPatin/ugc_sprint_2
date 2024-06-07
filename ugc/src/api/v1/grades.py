from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fast_depends import Depends, inject
from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.grades import GradeCreate, GradeUpdate
from src.services.grades import GradeManager, get_grade_manager

routers = Blueprint("grades", __name__, url_prefix=PREFIX_BASE_ROUTE + "/grades")


@routers.route("/", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get_all(user: AuthUser, grade_manager: Annotated[GradeManager, Depends(get_grade_manager)]):
    grades = grade_manager.find_all(user_id=user.id)

    return jsonify([grade.model_dump() for grade in grades]), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["POST"], strict_slashes=False)
@check_access_token
@inject
def create(user: AuthUser, film_id: UUID, grade_manager: Annotated[GradeManager, Depends(get_grade_manager)]):
    request_data = request.json
    try:
        data_model = GradeCreate(
            user_id=user.id, film_id=str(film_id), rating=request_data.get("rating") if request_data else None
        )

        grade = grade_manager.create(data_model.model_dump())

        return jsonify(grade.model_dump()), HTTPStatus.CREATED

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get(user: AuthUser, film_id: UUID, grade_manager: Annotated[GradeManager, Depends(get_grade_manager)]):
    grade = grade_manager.find_one({"user_id": user.id, "film_id": str(film_id)})

    if grade is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    return jsonify(grade.model_dump()), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["PATCH"], strict_slashes=False)
@check_access_token
@inject
def update(user: AuthUser, film_id: UUID, grade_manager: Annotated[GradeManager, Depends(get_grade_manager)]):
    request_data = request.json
    try:
        data_model = GradeUpdate.model_validate(request_data)
        grade_exist = grade_manager.find_one({"user_id": user.id, "film_id": str(film_id)})
        if grade_exist is None:
            abort(HTTPStatus.NOT_FOUND, description="Film not found")

        grade = grade_manager.update(grade_exist, data_model.rating)

        return jsonify(grade.model_dump()), HTTPStatus.OK

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["DELETE"], strict_slashes=False)
@check_access_token
@inject
def delete(user: AuthUser, film_id: UUID, grade_manager: Annotated[GradeManager, Depends(get_grade_manager)]):
    grade = grade_manager.find_one({"user_id": user.id, "film_id": str(film_id)})

    if grade is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    grade_manager.delete(grade)

    return jsonify({}), HTTPStatus.NO_CONTENT
