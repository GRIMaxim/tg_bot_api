from enum import Enum


class ErrorMessages(str, Enum):
    """Сообщения об ошибках, используемые в HTTP-исключениях."""

    USER_IS_ALREADY_EXIST = "User is already exist"
    USER_NOT_FOUND = "User not found"
