from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fast_depends import Depends, inject
from flask import Blueprint, abort, jsonify, request
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.db.repositories import ReviewRepository, get_review_repository
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.reviews import ReviewModel, ReviewUpdate

routers = Blueprint("reviews", __name__, url_prefix=PREFIX_BASE_ROUTE + "/reviews")


@routers.route("/", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get_all(user: AuthUser, repository: Annotated[ReviewRepository, Depends(get_review_repository)]):
    reviews = repository.find_all({"author": user.id})

    return jsonify([review.model_dump() for review in reviews]), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["POST"], strict_slashes=False)
@check_access_token
@inject
def create(user: AuthUser, film_id: UUID, repository: Annotated[ReviewRepository, Depends(get_review_repository)]):
    request_data = request.json
    try:
        data_model = ReviewModel(
            film_id=str(film_id), author=user.id, text=request_data.get("text") if request_data else None
        )

        favorite = repository.create(data_model.model_dump())

        return jsonify(favorite.model_dump()), HTTPStatus.CREATED

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["GET"], strict_slashes=False)
@inject
def get(film_id: UUID, repository: Annotated[ReviewRepository, Depends(get_review_repository)]):
    reviews = repository.find_all({"film_id": str(film_id)})

    return jsonify([review.model_dump() for review in reviews]), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["PATCH"], strict_slashes=False)
@check_access_token
@inject
def update(user: AuthUser, film_id: UUID, repository: Annotated[ReviewRepository, Depends(get_review_repository)]):
    request_data = request.json
    try:
        data_model = ReviewUpdate.model_validate(request_data)
        review_exist = repository.find_one({"author": user.id, "film_id": str(film_id)})

        if review_exist is None:
            abort(HTTPStatus.NOT_FOUND, description="Review not found")

        review = repository.update(review_exist, data_model.text)

        return jsonify(review.model_dump()), HTTPStatus.OK

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["DELETE"], strict_slashes=False)
@check_access_token
@inject
def delete(user: AuthUser, film_id: UUID, repository: Annotated[ReviewRepository, Depends(get_review_repository)]):
    review = repository.find_one({"author": user.id, "film_id": str(film_id)})

    if review is None:
        abort(HTTPStatus.NOT_FOUND, description="Review not found")

    repository.delete(review)

    return jsonify({}), HTTPStatus.NO_CONTENT
