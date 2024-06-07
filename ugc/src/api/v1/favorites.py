from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fast_depends import Depends, inject
from flask import Blueprint, abort, jsonify
from pydantic import ValidationError

from src.core.config import PREFIX_BASE_ROUTE
from src.db.repositories import FavoriteRepository, get_favorite_repository
from src.helpers.check_token import check_access_token
from src.models.auth import AuthUser
from src.models.favorites import FavoriteModel

routers = Blueprint("favorites", __name__, url_prefix=PREFIX_BASE_ROUTE + "/favorites")


@routers.route("/", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get_all(user: AuthUser, repository: Annotated[FavoriteRepository, Depends(get_favorite_repository)]):
    favorites = repository.find_all(condition={"user_id": user.id})

    return jsonify([favorite.model_dump() for favorite in favorites]), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["POST"], strict_slashes=False)
@check_access_token
@inject
def create(user: AuthUser, film_id: UUID, repository: Annotated[FavoriteRepository, Depends(get_favorite_repository)]):
    try:
        data_model = FavoriteModel(
            user_id=user.id,
            film_id=str(film_id),
        )

        favorite = repository.create(data_model.model_dump())

        return jsonify(favorite.model_dump()), HTTPStatus.CREATED

    except ValidationError:
        abort(HTTPStatus.BAD_REQUEST, description="Missing required parameter")


@routers.route("/<uuid:film_id>", methods=["GET"], strict_slashes=False)
@check_access_token
@inject
def get(user: AuthUser, film_id: UUID, repository: Annotated[FavoriteRepository, Depends(get_favorite_repository)]):
    favorite = repository.find_one({"user_id": user.id, "film_id": str(film_id)})

    if favorite is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    return jsonify(favorite.model_dump()), HTTPStatus.OK


@routers.route("/<uuid:film_id>", methods=["DELETE"], strict_slashes=False)
@check_access_token
@inject
def delete(user: AuthUser, film_id: UUID, repository: Annotated[FavoriteRepository, Depends(get_favorite_repository)]):
    favorite = repository.find_one({"user_id": user.id, "film_id": str(film_id)})

    if favorite is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    repository.delete(favorite)

    return jsonify({}), HTTPStatus.NO_CONTENT
