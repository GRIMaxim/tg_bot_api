from typing import Any, ClassVar

from faker import Faker

from src.user_data.crud import CRUDUserData
from src.user_chat.crud import CRUDUserChat


fk = Faker()


class TestCRUDUserChat:
    """Сборка тестов для CRUDUserChat."""

    user: ClassVar[dict[str, Any]] = {"user_id": fk.random_int(), "username": fk.name()}
    chats: ClassVar[list[str]] = [fk.name() for _ in range(100)]

    async def test_create_get(
        self,
        user_data_db: CRUDUserData,
        user_chat_db: CRUDUserChat,
    ) -> None:
        """Тестирование CRUDUserChat.create (overload) и CRUDUserChat.get (overload)."""
        await user_data_db.create(self.user)
        await user_chat_db.add_chats(
            {"user_id": self.user["user_id"], "chats": self.chats},
        )
        db_chats = await user_chat_db.get_chats(self.user["user_id"])

        assert db_chats
        assert self.chats == db_chats

    async def test_get_chats_from_user_data(self, user_data_db: CRUDUserData) -> None:
        """Тестирование CRUDUserChat.get_by_user_id_with_fk.

        Вынесена в TestCRUDUserChat, поскольку относится к связанной таблице user_chat и
        используются тестовые данные self.chats.
        """
        user_data = await user_data_db.get_by_user_id_with_fk(self.user["user_id"])

        assert user_data.chats
        assert self.chats == user_data.chats

    async def test_delete_chats(self, user_chat_db: CRUDUserChat) -> None:
        """Тестирование CRUDUserChat.delete_chats."""
        data = {"user_id": self.user["user_id"], "chats": self.chats[:50]}
        await user_chat_db.delete_chats(data)

        db_chats = await user_chat_db.get_chats(self.user["user_id"])

        assert db_chats
        assert self.chats[50:] == db_chats

    async def test_delete_all(self, user_chat_db: CRUDUserChat) -> None:
        """Тестирование CRUDUserChat.delete_chats."""
        await user_chat_db.delete_all(self.user["user_id"])

        db_chats = await user_chat_db.get_chats(self.user["user_id"])

        assert not db_chats
