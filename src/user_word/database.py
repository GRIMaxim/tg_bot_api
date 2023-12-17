from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.config import Base


class UserWord(Base):
    """Схема данных для таблицы с ключевыми/исключающими словами пользователей."""

    __tablename__ = "user_word"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.user_id"))
    word: Mapped[str] = mapped_column(nullable=True)
    is_key: Mapped[bool] = mapped_column(nullable=True)

