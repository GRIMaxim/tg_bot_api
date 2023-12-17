from typing import Any, ClassVar

from faker import Faker
from fastapi import status
from httpx import AsyncClient, Response

from src.user_word.constants import RouterPaths as WordRouterPaths
from src.user_data.constants import RouterPaths as UserRouterPaths

fk = Faker()


class TestUserWordRouter:
    """Сборка тестов для роутера user_word."""

    user_id: ClassVar[int] = fk.random_int()
    words: ClassVar[list[dict[str, Any]]] = [
        {"word": fk.name(), "is_key": i % 2 == 0} for i in range(100)
    ]

    async def test_create_get(self, client: AsyncClient) -> None:
        """Тестирование добавления и получения списка слов."""
        response: Response = await client.post(
            UserRouterPaths.CREATE_USER,
            json={"user_id": self.user_id},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.post(
            WordRouterPaths.ADD_WORDS,
            json={"user_id": self.user_id, "words": self.words},
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            WordRouterPaths.GET_WORDS + f"?user_id={self.user_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["user_id"] == self.user_id
        assert response_data["words"] == self.words

    async def test_delete_some_keys(self, client: AsyncClient) -> None:
        """Тестирование удаления ключевых слов."""
        response: Response = await client.put(
            WordRouterPaths.DELETE_WORD_LIST,
            json={
                "user_id": self.user_id,
                "words": [data["word"] for data in self.words[:10] if data["is_key"]],
                "is_key": True,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            WordRouterPaths.GET_WORDS + f"?user_id={self.user_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["user_id"] == self.user_id
        assert {data["word"] for data in response_data["words"] if data["is_key"]} == {
            data["word"] for data in self.words[10:] if data["is_key"]
        }

    async def test_delete_some_excepts(self, client: AsyncClient) -> None:
        """Тестирование удаления исключающих слов."""
        response: Response = await client.put(
            WordRouterPaths.DELETE_WORD_LIST,
            json={
                "user_id": self.user_id,
                "words": [data["word"] for data in self.words[:10] if not data["is_key"]],
                "is_key": False,
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            WordRouterPaths.GET_WORDS + f"?user_id={self.user_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["user_id"] == self.user_id
        assert {data["word"] for data in response_data["words"] if not data["is_key"]} == {
            data["word"] for data in self.words[10:] if not data["is_key"]
        }

    async def test_delete_all_keys(self, client: AsyncClient) -> None:
        """Тестирование удаления всех ключевых слов."""
        response: Response = await client.delete(
            WordRouterPaths.DELETE_WORDS_BY_KEY + f"?user_id={self.user_id}&is_key=true",
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            WordRouterPaths.GET_WORDS + f"?user_id={self.user_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["user_id"] == self.user_id
        assert any(not data["is_key"] for data in response_data["words"])

    async def test_delete_all_excepts(self, client: AsyncClient) -> None:
        """Тестирование удаления всех исключающих слов."""
        response: Response = await client.delete(
            WordRouterPaths.DELETE_WORDS_BY_KEY + f"?user_id={self.user_id}&is_key=false",
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            WordRouterPaths.GET_WORDS + f"?user_id={self.user_id}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["user_id"] == self.user_id
        assert not response_data["words"]
