from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fast_depends import Depends, inject
from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.db.repositories import GradeRepository, get_grade_repository
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.grades import GradeFilmCreate, GradeUpdate

routers = Blueprint("grades", __name__, url_prefix=PREFIX_BASE_ROUTE + "/grades")


@routers.route("/", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get_all(user: AuthUser, repository: Annotated[GradeRepository, Depends(get_grade_repository)]):
    """Просмотр списка фильмов оцененных пользователем."""
    grades = repository.find_all(condition={"user_id": user.id})

    return jsonify([grade.model_dump() for grade in grades]), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["POST"], strict_slashes=False)
@check_access_token
@inject
def create(user: AuthUser, film_id: UUID, repository: Annotated[GradeRepository, Depends(get_grade_repository)]):
    """Добавление оценки к фильму пользователем."""
    request_data = request.json
    try:
        data_model = GradeFilmCreate(
            user_id=user.id, film_id=str(film_id), rating=request_data.get("rating") if request_data else None
        )

        grade = repository.find_one({"user_id": data_model.user_id, "film_id": data_model.film_id})
        if grade is None:
            grade = repository.create(data_model.model_dump())

        return jsonify(grade.model_dump()), HTTPStatus.CREATED

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get(user: AuthUser, film_id: UUID, repository: Annotated[GradeRepository, Depends(get_grade_repository)]):
    """Просмотр оценки к фильму."""
    grade = repository.find_one({"user_id": user.id, "film_id": str(film_id)})

    if grade is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    return jsonify(grade.model_dump()), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["PATCH"], strict_slashes=False)
@check_access_token
@inject
def update(user: AuthUser, film_id: UUID, repository: Annotated[GradeRepository, Depends(get_grade_repository)]):
    """Обновление оценки к фильму пользователем."""
    request_data = request.json
    try:
        data_model = GradeUpdate.model_validate(request_data)
        grade_exist = repository.find_one({"user_id": user.id, "film_id": str(film_id)})
        if grade_exist is None:
            abort(HTTPStatus.NOT_FOUND, description="Film not found")

        grade = repository.update(grade_exist, data_model.rating)

        return jsonify(grade.model_dump()), HTTPStatus.OK

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["DELETE"], strict_slashes=False)
@check_access_token
@inject
def delete(user: AuthUser, film_id: UUID, repository: Annotated[GradeRepository, Depends(get_grade_repository)]):
    """Удаление оценки к фильму."""
    grade = repository.find_one({"user_id": user.id, "film_id": str(film_id)})

    if grade is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    repository.delete(grade)

    return jsonify({}), HTTPStatus.NO_CONTENT
