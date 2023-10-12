from enum import Enum


class ErrorMessages(str, Enum):
    """Сообщения об ошибках, используемые в HTTP-исключениях."""

    USER_IS_ALREADY_EXIST = "User is already exist"
    USER_NOT_FOUND = "User not found"


class RouterPaths(str, Enum):
    """Перечисление путей для роутера user_data."""

    CREATE_USER = "/user/data/"
    GET_USER = "/user/data/" # noqa:PIE796
    GET_ALL_USER_DATA = "/user/data/all_with_fk"
    GET_ALL_USERS = "/user/data/all"
    UPDATE_USER = "/user/data/" # noqa:PIE796
