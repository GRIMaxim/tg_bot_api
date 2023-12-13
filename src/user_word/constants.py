from enum import Enum


class RouterPaths(str, Enum):
    """Перечисление путей для роутера user_word."""

    ADD_WORDS = "/user/words/"
    GET_WORDS = "/user/words/all"

    DELETE_WORDS = "/user/words/"  # noqa:PIE796
    DELETE_ALL_CHATS = "/user/words/all"  # noqa: PIE796
