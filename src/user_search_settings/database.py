from datetime import datetime

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from src.config import Base


class UserSearchSettings(Base):
    """Схема данных для настроек поиска по датам."""

    __tablename__ = "user_search_settings"

    user_id: Mapped[int] = mapped_column(ForeignKey("user_data.user_id"))
    start_date: Mapped[datetime] = mapped_column(
        __type_pos=TIMESTAMP(timezone=True),
        nullable=True,
    )
    end_date: Mapped[datetime] = mapped_column(
        __type_pos=TIMESTAMP(timezone=True),
        nullable=True,
    )
