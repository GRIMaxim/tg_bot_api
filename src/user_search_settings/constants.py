from enum import Enum


class RouterPaths(str, Enum):
    """Перечисление путей для роутера user_search_settings."""

    GET_SETTINGS = "/user/settings/"
    UPDATE_SETTINGS = "/user/settings/"  # noqa:PIE796
