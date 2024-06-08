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
from src.models.events import FavoriteEvent
from src.models.favorites import FavoriteCreate
from src.services.handlers import EventHandler, get_event_handler

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
def create(
    user: AuthUser,
    film_id: UUID,
    repository: Annotated[FavoriteRepository, Depends(get_favorite_repository)],
    event_handler: Annotated[EventHandler, Depends(get_event_handler)],
):
    try:
        data_model = FavoriteCreate(
            user_id=user.id,
            film_id=str(film_id),
        )

        favorite = repository.find_one({"user_id": data_model.user_id, "film_id": data_model.film_id})
        if favorite is None:
            favorite = repository.create(data_model.model_dump())

        event_model = FavoriteEvent(user_id=user.id, film_id=str(film_id), action="create")
        event_handler.send_message(topic="favorites", key=event_model.film_id, data=event_model)

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
def delete(
    user: AuthUser,
    film_id: UUID,
    repository: Annotated[FavoriteRepository, Depends(get_favorite_repository)],
    event_handler: Annotated[EventHandler, Depends(get_event_handler)],
):
    favorite = repository.find_one({"user_id": user.id, "film_id": str(film_id)})

    if favorite is None:
        abort(HTTPStatus.NOT_FOUND, description="Film not found")

    repository.delete(favorite)

    event_model = FavoriteEvent(user_id=user.id, film_id=str(film_id), action="delete")
    event_handler.send_message(topic="favorites", key=event_model.film_id, data=event_model)

    return jsonify({}), HTTPStatus.NO_CONTENT
