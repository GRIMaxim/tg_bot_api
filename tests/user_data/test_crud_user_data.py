from typing import ClassVar

import pytest
from faker import Faker
from src.user_data.crud import user_data_db
from src.user_data.schemas import CreateUser

fk = Faker()


class TestCRUDUser:
    """Класс с собранием тестов, относящимся к CRUDUserData."""

    test_user: ClassVar[CreateUser] = CreateUser(user_id=1234, username="test")

    @pytest.mark.asyncio()
    async def test_get_user_by_id(self) -> None:
        """Тестирование CRUDUserData.get_by_user_id."""
        await user_data_db.create(self.test_user)

        created_user = await user_data_db.get_by_user_id(self.test_user.user_id)
        assert created_user
        assert created_user.user_id == self.test_user.user_id
        assert created_user.username == self.test_user.username
        assert created_user.create_at
        assert not created_user.start_subs_at
        assert not created_user.end_subs_at
        assert not created_user.is_subs_active
        assert not created_user.is_trial_used
        assert not created_user.online_search_active

        not_user = await user_data_db.get_by_user_id(created_user.user_id + 10000)
        assert not_user is None

    @pytest.mark.asyncio()
    async def test_get_user_by_username(self) -> None:
        """Тестирование CRUDUserData.get_by_username."""
        assert self.test_user.username
        created_user = await user_data_db.get_by_username(self.test_user.username)
        assert created_user
        assert created_user.user_id == self.test_user.user_id
        assert created_user.username == self.test_user.username
        assert created_user.create_at
        assert not created_user.start_subs_at
        assert not created_user.end_subs_at
        assert not created_user.is_subs_active
        assert not created_user.is_trial_used
        assert not created_user.online_search_active

        not_user = await user_data_db.get_by_username(self.test_user.username + "abc")
        assert not_user is None
