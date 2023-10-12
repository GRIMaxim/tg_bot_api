from enum import Enum


class ErrorMessages(str, Enum):
    """Сообщения об ошибках, используемые в HTTP-исключениях."""

    USER_IS_ALREADY_EXIST = "User is already exist"
    USER_NOT_FOUND = "User not found"


class RouterPaths(str, Enum):
    """Перечисление путей для роутера user_data."""

    CREATE_USER = "/user/"
    GET_USER = "/user/"
    GET_ALL_USER_DATA = "/user/all"
    GET_ALL_USERS = "/user/all"
    UPDATE_USER = "/user/"
