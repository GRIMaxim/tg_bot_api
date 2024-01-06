from .database import UserSearchSettings
from .crud import CRUDUserSearchSettings


def get_user_search_settings_db() -> CRUDUserSearchSettings:
    """Фабрика для получения экземпляра CRUDUserSearchSettings."""
    return CRUDUserSearchSettings(UserSearchSettings)
