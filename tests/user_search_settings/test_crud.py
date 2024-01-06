from typing import ClassVar
from datetime import datetime, timedelta, UTC

from faker import Faker

from src.user_data.schemas import UserCreate
from src.user_data.crud import CRUDUserData
from src.user_search_settings.crud import CRUDUserSearchSettings
from src.user_search_settings.schemas import SettingsCreate, SettingsUpdate


fk = Faker()


class TestCRUDUserSearchSettings:
    """Сборка тестов для CRUDUserSearchSettings."""

    test_user: ClassVar[UserCreate] = UserCreate(
        user_id=fk.random_int(),
        username=fk.name(),
    )
    test_settings: ClassVar[SettingsCreate] = SettingsCreate(
        user_id=test_user.user_id,
        start_date=datetime.now(tz=UTC),
        end_date=datetime.now(tz=UTC) + timedelta(days=2),
    )

    async def test_create_get(
        self,
        user_search_settings_db: CRUDUserSearchSettings,
        user_data_db: CRUDUserData,
    ) -> None:
        """Тестирование CRUDBase.create и CRUDUserSearchSettings.get_settings_by_user_id."""
        await user_data_db.create(self.test_user)
        await user_search_settings_db.create(self.test_settings)
        settings_db = await user_search_settings_db.get_settings_by_user_id(
            self.test_user.user_id
        )
        assert settings_db.user_id == self.test_settings.user_id
        assert settings_db.start_date == self.test_settings.start_date
        assert settings_db.end_date == self.test_settings.end_date

    async def test_update_settings(
        self, user_search_settings_db: CRUDUserSearchSettings
    ) -> None:
        """Тестирование CRUDBase.create и CRUDUserSearchSettings.get_settings_by_user_id."""
        updated_settings = SettingsUpdate(
            user_id=self.test_settings.user_id,
            start_date=self.test_settings.start_date + timedelta(days=1),
            end_date=self.test_settings.end_date + timedelta(days=1),
        )
        await user_search_settings_db.update_settings(updated_settings)
        settings_db = await user_search_settings_db.get_settings_by_user_id(
            self.test_user.user_id
        )
        assert settings_db.user_id == updated_settings.user_id
        assert settings_db.start_date == updated_settings.start_date
        assert settings_db.end_date == updated_settings.end_date
