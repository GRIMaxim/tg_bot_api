from .database import UserChat
from .crud import CRUDUserChat


def get_user_chat_db() -> CRUDUserChat:
    """Фабрика для получения экземпляра CRUDUserChat."""
    return CRUDUserChat(UserChat)
