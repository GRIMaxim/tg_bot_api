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

    async def test_create_get(self, client: AsyncClient) -> None:
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
