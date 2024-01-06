from datetime import datetime, timedelta, UTC
from typing import ClassVar, Any

from faker import Faker
from httpx import AsyncClient
from starlette import status

from src.user_data.crud import CRUDUserData
from src.user_search_settings.crud import CRUDUserSearchSettings
from src.user_search_settings.constants import RouterPaths

fk = Faker()


class TestUserSearchSettingsRouter:
    """Сборка тестов для роутера user_search_settings."""

    test_user: ClassVar[dict[str, Any]] = {
        "user_id": fk.random_int(),
    }
    test_settings: ClassVar[dict[str, Any]] = {
        "user_id": test_user["user_id"],
        "start_date": datetime.now(tz=UTC),
        "end_date": datetime.now(tz=UTC) + timedelta(days=1),
    }

    async def test_get_settings(
        self,
        user_search_settings_db: CRUDUserSearchSettings,
        user_data_db: CRUDUserData,
        client: AsyncClient,
    ) -> None:
        """Тестирование получения настроек пользователя для мгновенного поиска."""
        await user_data_db.create(self.test_user)
        await user_search_settings_db.create(self.test_settings)
        response = await client.get(
            RouterPaths.GET_SETTINGS, params={"user_id": self.test_settings["user_id"]},
        )
        assert response.status_code == status.HTTP_200_OK
        settings = response.json()
        assert settings["user_id"] == self.test_settings["user_id"]
        assert datetime.fromisoformat(settings["start_date"]) == self.test_settings["start_date"]
        assert datetime.fromisoformat(settings["end_date"]) == self.test_settings["end_date"]

    async def test_update_settings(self, client: AsyncClient) -> None:
        """Тестирование обновления настроек пользователя для мгновенного поиска."""
        updated_settings = self.test_settings.copy()
        updated_settings["start_date"] = (updated_settings["start_date"] + timedelta(
            days=1,
        )).isoformat()
        updated_settings["end_date"] = (updated_settings["end_date"] + timedelta(days=1)).isoformat()
        response = await client.put(RouterPaths.UPDATE_SETTINGS, json=updated_settings)
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await client.get(
            RouterPaths.GET_SETTINGS, params={"user_id": self.test_settings["user_id"]},
        )
        assert response.status_code == status.HTTP_200_OK
        settings = response.json()
        assert settings["user_id"] == updated_settings["user_id"]
        assert datetime.fromisoformat(settings["start_date"]) == datetime.fromisoformat(updated_settings["start_date"])
        assert datetime.fromisoformat(settings["end_date"]) == datetime.fromisoformat(updated_settings["end_date"])
