from http import HTTPStatus
from typing import Annotated, Any
from uuid import UUID

from fast_depends import Depends, inject
from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.db.repositories import (
    ReviewGradeRepository,
    ReviewRepository,
    get_review_grade_repository,
    get_review_repository,
)
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.events import GradeReviewEvent, ReviewEvent
from src.models.grades import GradeReviewCreate, GradeUpdate
from src.models.reviews import ReviewCreate, ReviewUpdate
from src.services.handlers import EventHandler, get_event_handler

routers = Blueprint("reviews", __name__, url_prefix=PREFIX_BASE_ROUTE + "/reviews")


@inject
def send_grade_event(
    data_event: dict[str, Any],
    event_handler: Annotated[EventHandler, Depends(get_event_handler)],
):
    event_model = GradeReviewEvent(**data_event)
    event_handler.send_message(topic="grades", key=event_model.review_id, data=event_model)


@routers.route("/", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get_all(user: AuthUser, repository: Annotated[ReviewRepository, Depends(get_review_repository)]):
    """Просмотр списка рецензий к фильмам пользователя."""
    reviews = repository.find_all({"author": user.id})

    return jsonify([review.model_dump() for review in reviews]), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["POST"], strict_slashes=False)
@check_access_token
@inject
def create(
    user: AuthUser,
    film_id: UUID,
    repository: Annotated[ReviewRepository, Depends(get_review_repository)],
    event_handler: Annotated[EventHandler, Depends(get_event_handler)],
):
    """Добавление рецензии к фильму пользователем."""
    request_data = request.json
    try:
        data_model = ReviewCreate(
            film_id=str(film_id), author=user.id, text=request_data.get("text") if request_data else None
        )

        favorite = repository.find_one({"author": data_model.author, "film_id": data_model.film_id})
        if favorite is None:
            favorite = repository.create(data_model.model_dump())

        event_model = ReviewEvent(film_id=str(film_id), author=user.id, action="create")
        event_handler.send_message(topic="reviews", key=event_model.film_id, data=event_model)

        return jsonify(favorite.model_dump()), HTTPStatus.CREATED

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["GET"], strict_slashes=False)
@inject
def get(film_id: UUID, repository: Annotated[ReviewRepository, Depends(get_review_repository)]):
    """Просмотр рецензии к фильму."""
    reviews = repository.find_all({"film_id": str(film_id)})

    return jsonify([review.model_dump() for review in reviews]), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["PATCH"], strict_slashes=False)
@check_access_token
@inject
def update(
    user: AuthUser,
    film_id: UUID,
    repository: Annotated[ReviewRepository, Depends(get_review_repository)],
    event_handler: Annotated[EventHandler, Depends(get_event_handler)],
):
    """Обновление рецензии к фильму пользователем."""
    request_data = request.json
    try:
        data_model = ReviewUpdate.model_validate(request_data)
        review = repository.find_one({"author": user.id, "film_id": str(film_id)})

        if review is None:
            abort(HTTPStatus.NOT_FOUND, description="Review not found")

        review_updated = repository.update_text(review, data_model.text)

        event_model = ReviewEvent(film_id=str(film_id), author=user.id, action="update")
        event_handler.send_message(topic="reviews", key=event_model.film_id, data=event_model)

        return jsonify(review_updated.model_dump()), HTTPStatus.OK

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["DELETE"], strict_slashes=False)
@check_access_token
@inject
def delete(
    user: AuthUser,
    film_id: UUID,
    repository: Annotated[ReviewRepository, Depends(get_review_repository)],
    event_handler: Annotated[EventHandler, Depends(get_event_handler)],
):
    """Удаление рецензии к фильму пользователем."""
    review = repository.find_one({"author": user.id, "film_id": str(film_id)})

    if review is None:
        abort(HTTPStatus.NOT_FOUND, description="Review not found")

    repository.delete(review)

    event_model = ReviewEvent(film_id=str(film_id), author=user.id, action="update")
    event_handler.send_message(topic="reviews", key=event_model.film_id, data=event_model)

    return jsonify({}), HTTPStatus.NO_CONTENT


@routers.route("/<uuid:review_id>/grade", methods=["POST"], strict_slashes=False)
@check_access_token
@inject
def create_grade(
    user: AuthUser,
    review_id: UUID,
    review_repository: Annotated[ReviewRepository, Depends(get_review_repository)],
    review_grade_repository: Annotated[ReviewGradeRepository, Depends(get_review_grade_repository)],
):
    """Добавление оценки к рецензии пользователем"""
    request_data = request.json

    review = review_repository.get(review_id)
    if review is None:
        abort(HTTPStatus.NOT_FOUND, description="Review not found")

    if review.author == user.id:
        abort(HTTPStatus.BAD_REQUEST, description="You cannot add a rating to your review.")

    try:
        data_model = GradeReviewCreate(
            user_id=user.id, review_id=str(review_id), rating=request_data.get("rating") if request_data else None
        )

        grade = review_grade_repository.find_one({"user_id": data_model.user_id, "review_id": data_model.review_id})
        if grade is None:
            grade = review_grade_repository.create(data_model.model_dump())

        send_grade_event(data_model.model_dump())  # type: ignore

        return jsonify(grade.model_dump()), HTTPStatus.CREATED

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:review_id>/grade", methods=["PATCH"], strict_slashes=False)
@check_access_token
@inject
def update_grade(
    user: AuthUser,
    review_id: UUID,
    repository: Annotated[ReviewGradeRepository, Depends(get_review_grade_repository)],
):
    """Обновление оценки к рецензии пользователем"""
    request_data = request.json

    try:
        data_model = GradeUpdate.model_validate(request_data)

        grade = repository.find_one({"user_id": user.id, "review_id": str(review_id)})
        if grade is None:
            abort(HTTPStatus.NOT_FOUND, description="Review not found")

        grade_updated = repository.update_rating(grade, data_model.rating)

        send_grade_event(grade_updated.model_dump())  # type: ignore

        return jsonify(grade_updated.model_dump()), HTTPStatus.OK

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:review_id>/grade", methods=["DELETE"], strict_slashes=False)
@check_access_token
@inject
def delete_grade(
    user: AuthUser,
    review_id: UUID,
    repository: Annotated[ReviewGradeRepository, Depends(get_review_grade_repository)],
):
    """Удаление оценки к рецензии пользователем"""
    grade = repository.find_one({"user_id": user.id, "review_id": str(review_id)})

    if grade is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    repository.delete(grade)

    send_grade_event({"user_id": user.id, "review_id": str(review_id), "rating": 0})  # type: ignore

    return jsonify({}), HTTPStatus.NO_CONTENT
