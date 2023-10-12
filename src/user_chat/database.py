from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.config import Base


class UserChat(Base):
    """Схема данных для таблицы с чатами пользователей."""

    __tablename__ = "user_chat"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.user_id"))
    chat_name: Mapped[str] = mapped_column(nullable=True)
