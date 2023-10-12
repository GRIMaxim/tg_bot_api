from typing import Any, ClassVar

from faker import Faker
from fastapi import status
from httpx import AsyncClient, Response

from src.user_chat.constants import RouterPaths as ChatRouterPaths
from src.user_data.constants import RouterPaths as UserRouterPaths

fk = Faker()


class TestUserChatRouter:
    """Сборка тестов для роутера user_chat."""

    length_chat_list = 50
    user: ClassVar[dict[str, Any]] = {"user_id": fk.random_int()}
    chats: ClassVar[list[str]] = [fk.name() for _ in range(length_chat_list)]

    async def test_create_get_chats(self, client: AsyncClient) -> None:
        """Тестирование добавления и получения списка чатов."""
        response: Response = await client.post(
            UserRouterPaths.CREATE_USER,
            json={"user_id": self.user["user_id"]},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.post(
            ChatRouterPaths.ADD_CHATS,
            json={"user_id": self.user["user_id"], "chats": self.chats},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            ChatRouterPaths.GET_CHATS + f"?user_id={self.user['user_id']}",
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["user_id"] == self.user["user_id"]
        assert response_data["chats"].sort() == self.chats.sort()

    async def test_create_empty_list(self, client: AsyncClient) -> None:
        """Тестирование добавления и получения списка чатов."""
        response = await client.post(
            ChatRouterPaths.ADD_CHATS,
            json={"user_id": self.user["user_id"], "chats": []},
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_delete_list_chat(self, client: AsyncClient) -> None:
        """Тестирование удаления заданного списка чатов."""
        response: Response = await client.put(
            ChatRouterPaths.DELETE_CHATS,
            json={
                "user_id": self.user["user_id"],
                "chats": self.chats[: self.length_chat_list // 2],
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            ChatRouterPaths.GET_CHATS + f"?user_id={self.user['user_id']}",
        )

        assert response.status_code == status.HTTP_200_OK

        response_data = response.json()
        assert response_data["user_id"] == self.user["user_id"]
        assert (
            response_data["chats"].sort()
            == self.chats[self.length_chat_list // 2 :].sort()
        )

    async def test_delete_all_chats(self, client: AsyncClient) -> None:
        """Тестирование удаления всех чатов пользователя."""
        response: Response = await client.delete(
            ChatRouterPaths.DELETE_ALL_CHATS + f"?user_id={self.user['user_id']}",
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            ChatRouterPaths.GET_CHATS + f"?user_id={self.user['user_id']}",
        )

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["user_id"] == self.user["user_id"]
        assert not response_data["chats"]
