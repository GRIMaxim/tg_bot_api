from enum import Enum


class RouterPaths(str, Enum):
    """Перечисление путей для роутера subscription."""

    CREATE_SUBSCRIPTION = "/subscription/"
    GET_SUBSCRIPTION = "/subscription/"  # noqa:PIE796
    GET_SUBSCRIPTIONS = "/subscription/all"
    UPDATE_SUBSCRIPTION = "/subscription/"  # noqa:PIE796
    DELETE_SUBSCRIPTIONS = "/subscription/"  # noqa:PIE796
