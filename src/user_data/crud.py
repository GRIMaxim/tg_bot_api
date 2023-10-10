from typing import TYPE_CHECKING, Any

from pydantic import BaseModel
from sqlalchemy import select, update

from src.crud import CRUDBase
from src.utils import async_execute

from .database import UserData
from .schemas import UserCreate, UserUpdate

if TYPE_CHECKING:
    from collections.abc import Sequence


class CRUDUserData(CRUDBase[UserData, UserCreate, UserUpdate]):
    """Определение и расширение класса CRUDBase для схемы данных UserData."""

    async def get_by_user_id(self, user_id: int) -> UserData | None:
        """Получение пользователя по user id.

        Возвращает UserData, если пользователь существует, в противном случае None.
        """
        query = select(self.model).where(self.model.user_id == user_id)
        result = await async_execute(query)
        user: UserData | None = result.scalar_one_or_none()

        return user

    async def get_by_username(self, username: str) -> UserData | None:
        """Получение пользователя по username.

        Возвращает UserData, если пользователь существует, в противном случае None.
        """
        query = select(self.model).where(self.model.username == username)
        result = await async_execute(query)
        user: UserData | None = result.scalar_one_or_none()

        return user

    async def update(
        self,
        data_update: UserUpdate | dict[str, Any],
    ) -> None:
        """Обновляет поля пользователя бд по заданному user_id или username.

        *data_update* - модель UserUpdate или Mapping, с полями UserData
        """
        if isinstance(data_update, BaseModel):
            data_update = data_update.model_dump()

        user_id, username = None, None
        if "user_id" in data_update:
            user_id = data_update.pop("user_id")
        if "username" in data_update:
            username = data_update.pop("username")

        query = (
            update(self.model)
            .where((self.model.user_id == user_id) | (self.model.username == username))
            .values(**data_update)
        )

        await async_execute(query)
