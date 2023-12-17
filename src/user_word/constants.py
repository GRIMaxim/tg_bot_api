from enum import Enum


class RouterPaths(str, Enum):
    """Перечисление путей для роутера user_word."""

    ADD_WORDS = "/user/words/"
    GET_WORDS = "/user/words/all"
    DELETE_WORD_LIST = "/user/words/"  # noqa:PIE796
    DELETE_WORDS_BY_KEY = "/user/words/all"  # noqa: PIE796
