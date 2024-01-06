from typing import Any
from collections.abc import Mapping

from sqlalchemy import update, select
from pydantic import BaseModel

from src.crud import CRUDBase
from src.utils import async_execute

from .database import UserSearchSettings
from .schemas import (
    SettingsCreate,
    SettingsUpdate,
)


class CRUDUserSearchSettings(CRUDBase[UserSearchSettings, SettingsCreate, SettingsUpdate]):
    """Методы CRUD для работы с таблицей user_search_settings."""

    async def get_settings_by_user_id(self, user_id: int) -> UserSearchSettings:
        """Получение настроек пользователя из базы данных.

        **Параметры**

        *user_id* - id пользователя telegram.
        """
        query = select(self.model).where(self.model.user_id == user_id)
        result = await async_execute(query)
        settings: UserSearchSettings = result.scalar_one()
        return settings

    async def update_settings(self, settings: SettingsUpdate | Mapping[str, Any]) -> None:
        """Обновляет настройки пользователя."""
        if isinstance(settings, BaseModel):
            settings = settings.model_dump()
        query = (update(self.model).
                 where(self.model.user_id == settings["user_id"]).
                 values(start_date=settings["start_date"], end_date=settings["end_date"]))
        await async_execute(query)
