from .constants import ErrorMessages
from src.exceptions import Conflict, NotFound


class UserNotFound(NotFound):
    """Исключение пользователь не найден (404)."""

    DETAIL = ErrorMessages.USER_NOT_FOUND


class UserIsAlreadyExist(Conflict):
    """Исключение пользователь уже существует (409)."""

    DETAIL = ErrorMessages.USER_IS_ALREADY_EXIST
