from enum import Enum


class RouterPaths(str, Enum):
    """Перечисление путей для роутера user_chat."""

    ADD_CHATS = "/user/chats/"
    GET_CHATS = "/user/chats/"  # noqa:PIE796
    DELETE_CHATS = "/user/chats/"  # noqa:PIE796
    DELETE_ALL_CHATS = "/user/chats/all"
