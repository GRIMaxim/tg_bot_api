from typing import Any
from collections.abc import Mapping, Sequence

from sqlalchemy import insert, delete, select
from pydantic import BaseModel

from src.crud import CRUDBase
from src.utils import async_execute

from .database import UserChat
from .schemas import ChatCreate, ChatUpdate, ChatDelete


class CRUDUserChat(CRUDBase[UserChat, ChatCreate, ChatUpdate]):
    """Методы CRUD для работы с таблицей user_chat."""

    async def add_chats(self, user_chats: ChatCreate | Mapping[str, Any]) -> None:
        """Добавление списка чатов в базу данных.

        **Параметры**

        *user_chats* - схема запроса на добавление списка чатов
        с обязательными полями 'user_id'(id пользователя telegram)
        и 'chats' (список с названиями чатов).
        """
        if isinstance(user_chats, BaseModel):
            user_chats = user_chats.model_dump()

        chat_list = [
            {"user_id": user_chats["user_id"], "chat_name": chat}
            for chat in user_chats["chats"]
        ]
        query = insert(self.model).values(chat_list)
        await async_execute(query)

    async def get_chats(self, user_id: int) -> Sequence[str]:
        """Получение списка чатов из базы данных.

        **Параметры**

        *user_id* - id пользователя telegram.
        """
        query = select(self.model.chat_name).where(self.model.user_id == user_id)
        result = await async_execute(query)
        return result.scalars().all()

    async def delete_chats(
        self,
        chats_for_delete: ChatDelete | Mapping[str, Any],
    ) -> None:
        """Удаляет заданный список чатов из бд.

        **Параметры**

        *chats_for_delete* - схема запроса на удаление списка чатов
        с обязательными полями 'user_id' и 'chats'.
        """
        if isinstance(chats_for_delete, BaseModel):
            chats_for_delete = chats_for_delete.model_dump()

        query = delete(self.model).where(
            (self.model.user_id == chats_for_delete["user_id"])
            & self.model.chat_name.in_(chats_for_delete["chats"]),
        )
        await async_execute(query)

    async def delete_all(self, user_id: int) -> None:
        """Удаляет все чаты из бд.

        **Параметры**

        *user_id* - id пользователя telegram.
        """
        query = delete(self.model).where(self.model.user_id == user_id)
        await async_execute(query)
