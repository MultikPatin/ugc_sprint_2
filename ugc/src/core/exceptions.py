from http import HTTPStatus

from werkzeug.exceptions import HTTPException


class ValidationException(HTTPException):
    code = HTTPStatus.BAD_REQUEST
    description = "Invalid request, missing required parameters"
