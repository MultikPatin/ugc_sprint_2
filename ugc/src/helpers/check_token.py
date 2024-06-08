import functools
import time
from http import HTTPStatus
from typing import Any

import jwt
from flask import abort, request
from jwt import DecodeError
from pydantic import ValidationError

from src.models.auth import AuthUser


def get_data_jwt(encode_jwt: str) -> dict[str, Any] | None:
    data_jwt = jwt.decode(encode_jwt, options={"verify_signature": False})
    return data_jwt if data_jwt["exp"] >= time.time() else None


def check_access_token(func):
    @functools.wraps(func)
    def checking(*args, **kwargs):
        cookies = request.cookies.to_dict()
        access_jwt = cookies.get("access_token")
        if access_jwt is None:
            abort(
                HTTPStatus.FORBIDDEN,
                description="Invalid authorization code.",
            )

        try:
            data_token = get_data_jwt(access_jwt)
            if data_token is None:
                abort(
                    HTTPStatus.FORBIDDEN,
                    description="Invalid authorization code.",
                )
            try:
                user = AuthUser.model_validate(data_token)
                kwargs["user"] = user
            except ValidationError:
                abort(
                    HTTPStatus.FORBIDDEN,
                    description="Invalid authorization code.",
                )
        except DecodeError:
            abort(
                HTTPStatus.FORBIDDEN,
                description="Invalid authorization code.",
            )

        return func(*args, **kwargs)

    return checking
