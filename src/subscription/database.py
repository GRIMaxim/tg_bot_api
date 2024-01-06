from sqlalchemy.orm import Mapped

from src.config import Base


class Subscription(Base):
    """Схема данных для таблицы с возможными подписками и их настройками."""

    __tablename__ = "subscription"

    subscription_name: Mapped[str]
    duration: Mapped[int]
    chat_limit: Mapped[int]
    word_limit: Mapped[int]
    is_visible: Mapped[bool]
