from datetime import datetime, UTC, timedelta
from typing import TYPE_CHECKING, Any, ClassVar

from faker import Faker
from fastapi import status
from httpx import AsyncClient

from src.user_data.constants import ErrorMessages, RouterPaths
from src.user_data.database import UserData
from src.user_data.schemas import UserRead

if TYPE_CHECKING:
    from httpx import Response


fk = Faker()


class TestUserRouter:
    """."""

    default_user: ClassVar[dict[str, Any]] = {
        "user_id": fk.random_int(),
        "username": fk.name(),
        "is_subs_active": False,
        "start_subs_at": None,
        "end_subs_at": None,
        "is_trial_used": False,
        "online_search_active": False,
    }

    user_without_username: ClassVar[dict[str, Any]] = {
        "user_id": fk.random_int(),
        "username": None,
        "is_subs_active": False,
        "start_subs_at": None,
        "end_subs_at": None,
        "is_trial_used": False,
        "online_search_active": False,
    }

    @staticmethod
    def check_fields(
        data_in: dict[str, Any] | UserData,
        data_correct: dict[str, Any],
    ) -> None:
        """Функция для проверки полей.

        **Параметры**

        *data_in* - входные данные

        *data_correct* - ожидаемые данные
        """
        if isinstance(data_in, UserData):
            data_in: UserRead = UserRead.model_validate(data_in)
            data_in = data_in.model_dump()

        assert data_in["user_id"] == data_correct["user_id"]
        assert data_in["username"] == data_correct["username"]
        assert data_in["is_subs_active"] == data_correct["is_subs_active"]
        assert data_in["create_at"]
        assert isinstance(datetime.fromisoformat(data_in["create_at"]), datetime)

        if isinstance(data_in["start_subs_at"], str) and isinstance(
            data_correct["start_subs_at"],
            str,
        ):
            data_in["start_subs_at"] = datetime.fromisoformat(data_in["start_subs_at"])
            data_correct["start_subs_at"] = datetime.fromisoformat(
                data_correct["start_subs_at"],
            )
        assert data_in["start_subs_at"] == data_correct["start_subs_at"]

        if isinstance(data_in["end_subs_at"], str) and isinstance(
            data_correct["end_subs_at"],
            str,
        ):
            data_in["end_subs_at"] = datetime.fromisoformat(data_in["end_subs_at"])
            data_correct["end_subs_at"] = datetime.fromisoformat(
                data_correct["end_subs_at"],
            )
        assert data_in["end_subs_at"] == data_correct["end_subs_at"]

        assert data_in["is_trial_used"] == data_correct["is_trial_used"]
        assert data_in["online_search_active"] == data_correct["online_search_active"]

    async def test_create_get_correct_user(self, client: AsyncClient) -> None:
        """Тестирование обработчика создания пользователя со всеми полями и его дальнейшее получение."""
        response: Response = await client.post(
            RouterPaths.CREATE_USER,
            json={
                "user_id": self.default_user["user_id"],
                "username": self.default_user["username"],
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            RouterPaths.GET_USER + f"?user_id={self.default_user['user_id']}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        self.check_fields(response_data, self.default_user)

    async def test_create_user_without_username(self, client: AsyncClient) -> None:
        """Тестирование обработчика создания пользователя только с полем user_id."""
        response: Response = await client.post(
            RouterPaths.CREATE_USER,
            json={
                "user_id": self.user_without_username["user_id"],
            },
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            RouterPaths.GET_USER + f"?user_id={self.user_without_username['user_id']}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data

        self.check_fields(response_data, self.user_without_username)

    async def test_create_user_repeat(self, client: AsyncClient) -> None:
        """Попытка создания существующего пользователя."""
        response: Response = await client.post(
            RouterPaths.CREATE_USER,
            json={
                "user_id": self.default_user["user_id"],
                "username": self.default_user["username"],
            },
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response_data["detail"] == ErrorMessages.USER_IS_ALREADY_EXIST

    async def test_get_user_by_username(self, client: AsyncClient) -> None:
        """Тестирование получения пользователя по username."""
        response = await client.get(
            RouterPaths.GET_USER + f"?username={self.default_user['username']}"
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        self.check_fields(response_data, self.default_user)

    async def test_get_uncreated_user(self, client: AsyncClient) -> None:
        """Попытка получения несуществующего пользователя."""
        response: Response = await client.get(
            RouterPaths.GET_USER + f"?user_id={fk.random_int()}&username={fk.name()}",
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["detail"] == ErrorMessages.USER_NOT_FOUND

    async def test_get_all_users(self, client: AsyncClient) -> None:
        """Тестирование получения всех пользователей."""
        response: Response = await client.get(RouterPaths.GET_ALL_USERS)
        created_users = [self.default_user, self.user_without_username]
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        for created_user in created_users:
            for response_user in response_data["users"]:
                if response_user["user_id"] == created_user["user_id"]:
                    self.check_fields(response_user, created_user)

    async def test_update_user(self, client: AsyncClient) -> None:
        """Тестирование обновления пользовательских данных."""
        self.user_without_username["is_subs_active"] = True
        self.user_without_username["start_subs_at"] = datetime.now(tz=UTC).isoformat()
        self.user_without_username["end_subs_at"] = (
            datetime.now(tz=UTC) + timedelta(days=7)
        ).isoformat()

        response: Response = await client.put(
            RouterPaths.UPDATE_USER, json=self.user_without_username
        )
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            RouterPaths.GET_USER + f"?user_id={self.user_without_username['user_id']}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data
        self.check_fields(response_data, self.user_without_username)

    async def test_update_user_by_username(self, client: AsyncClient) -> None:
        """Тестирование обновления пользовательских данных."""
        user_id = self.default_user.pop("user_id")
        self.default_user["end_subs_at"] = (
            datetime.now(tz=UTC) + timedelta(days=7)
        ).isoformat()
        self.default_user["is_trial_used"] = True
        self.default_user["online_search_active"] = True

        response: Response = await client.put(
            RouterPaths.UPDATE_USER, json=self.default_user
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_202_ACCEPTED

        self.default_user["user_id"] = user_id

        response = await client.get(
            RouterPaths.GET_USER + f"?user_id={self.default_user['user_id']}",
        )
        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data

        self.check_fields(response_data, self.default_user)

    async def test_update_uncreated_user(self, client: AsyncClient) -> None:
        """Попытка обновления данных несуществующего пользователя."""
        response: Response = await client.put(
            RouterPaths.UPDATE_USER,
            json={"user_id": fk.random_int(), "is_trial_used": True},
        )
        response_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response_data["detail"] == ErrorMessages.USER_NOT_FOUND
        
    async def test_get_chats_with_user_data(self, client: AsyncClient) -> None:
        """Получение данных о пользователе и списка его чатов."""
