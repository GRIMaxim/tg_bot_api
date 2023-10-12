from .database import UserData
from .crud import CRUDUserData


def get_user_data_db() -> CRUDUserData:
    """Фабрика для получения экземпляра CRUDUserData."""
    return CRUDUserData(UserData)
