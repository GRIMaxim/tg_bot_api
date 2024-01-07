from typing import Any, ClassVar

from faker import Faker
from fastapi import status
from httpx import AsyncClient, Response

from src.subscription.constants import RouterPaths as SubscriptionRouterPaths

fk = Faker()


class TestSubscriptionRouter:
    """Сборка тестов для роутера subscription."""

    test_subscription: ClassVar[dict[str, Any]] = {
        "subscription_name": "FIRST",
        "duration": 12,
        "chat_limit": 20,
        "word_limit": 15,
        "is_visible": False,
    }

    async def test_create_get_subscription(self, client: AsyncClient) -> None:
        """Тестирование добавления и получения подписки."""
        response: Response = await client.post(
            SubscriptionRouterPaths.CREATE_SUBSCRIPTION,
            json=self.test_subscription,
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            SubscriptionRouterPaths.GET_SUBSCRIPTION, params={"pk": 1}
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data == self.test_subscription

    async def test_update(self, client: AsyncClient) -> None:
        """Тестирование обновления данных о подписке."""
        updated_data = self.test_subscription.copy()
        updated_data["is_visible"] = True
        updated_data["chat_limit"] = 100

        response = await client.put(
            SubscriptionRouterPaths.UPDATE_SUBSCRIPTION,
            json=updated_data,
        )
        assert response.status_code == status.HTTP_202_ACCEPTED
        response = await client.get(
            SubscriptionRouterPaths.GET_SUBSCRIPTION, params={"pk": 1}
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data == updated_data

    async def test_delete_list_subscription(self, client: AsyncClient) -> None:
        """Тестирование удаления заданного списка чатов."""
