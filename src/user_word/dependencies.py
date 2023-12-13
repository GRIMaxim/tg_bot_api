from .database import UserWord
from .crud import CRUDUserWord


def get_user_word_db() -> CRUDUserWord:
    """Фабрика для получения экземпляра CRUDUserWord."""
    return CRUDUserWord(UserWord)
