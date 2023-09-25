from typing import TYPE_CHECKING

from sqlalchemy import select

from src.crud_base import CRUDBase
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
        user: Sequence[UserData] | None = result.one_or_none()

        return user[0] if user is not None else None

    async def get_by_username(self, username: str) -> UserData | None:
        """Получение пользователя по username.

        Возвращает UserData, если пользователь существует, в противном случае None.
        """
        query = select(self.model).where(self.model.username == username)
        result = await async_execute(query)
        user: Sequence[UserData] | None = result.one_or_none()

        return user[0] if user is not None else None


user_data_db = CRUDUserData(UserData)
