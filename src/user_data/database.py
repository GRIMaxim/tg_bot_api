from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config import Base


class UserData(Base):
    """Схема данных для таблицы с пользователями."""

    __tablename__ = "user_data"

    user_id: Mapped[int] = mapped_column(__type_pos=BigInteger, nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_subs_active: Mapped[bool] = mapped_column(default=False)
    create_at: Mapped[datetime] = mapped_column(__type_pos=TIMESTAMP(timezone=True), default=datetime.now(tz=UTC))
    start_subs_at: Mapped[datetime] = mapped_column(__type_pos=TIMESTAMP(timezone=True), nullable=True)
    end_subs_at: Mapped[datetime] = mapped_column(__type_pos=TIMESTAMP(timezone=True), nullable=True)
    is_trial_used: Mapped[bool] = mapped_column(default=False)
    online_search_active: Mapped[bool] = mapped_column(default=False)

    chats: Mapped[list["UserChat"]] = relationship(lazy="selectin")
    