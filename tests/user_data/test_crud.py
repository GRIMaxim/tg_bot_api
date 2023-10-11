from typing import Any, ClassVar

from faker import Faker

from src.user_data.crud import CRUDUserData
from src.user_data.schemas import UserCreate


fk = Faker()


class TestCRUDUser:
    """Класс с собранием тестов, относящимся к CRUDUserData."""

    test_user: ClassVar[UserCreate] = UserCreate(user_id=fk.random_int(), username=fk.name())
    update_without_username: ClassVar[dict[str, Any]] = {
        "user_id": test_user.user_id,
        "is_subs_active": True,
        "is_trial_used": False,
        "online_search_active": True,
    }
    update_without_user_id: ClassVar[dict[str, Any]] = {
        "username": test_user.username,
        "is_subs_active": False,
        "online_search_active": False,
    }

    async def test_get_user_by_id(self, user_data_db: CRUDUserData) -> None:
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

    async def test_get_user_by_username(self, user_data_db: CRUDUserData) -> None:
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

    async def test_update_user(self, user_data_db: CRUDUserData) -> None:
        """Тестирование CRUDUserData.update (overload)."""
        await user_data_db.update(self.update_without_username)

        update_1 = await user_data_db.get_by_user_id(self.test_user.user_id)
        assert update_1
        assert update_1.user_id == self.test_user.user_id
        assert update_1.username == self.test_user.username
        assert update_1.create_at
        assert not update_1.start_subs_at
        assert not update_1.end_subs_at
        assert update_1.is_subs_active == self.update_without_username["is_subs_active"]
        assert update_1.is_trial_used == self.update_without_username["is_trial_used"]
        assert (
            update_1.online_search_active
            == self.update_without_username["online_search_active"]
        )

        await user_data_db.update(self.update_without_user_id)
        update_2 = await user_data_db.get_by_username(self.test_user.username)

        assert update_2
        assert update_2.user_id == self.test_user.user_id
        assert update_2.username == self.test_user.username
        assert update_2.create_at
        assert not update_2.start_subs_at
        assert not update_2.end_subs_at
        assert update_2.is_subs_active == self.update_without_user_id["is_subs_active"]
        assert update_2.is_trial_used == self.update_without_username["is_trial_used"]
        assert (
            update_2.online_search_active
            == self.update_without_user_id["online_search_active"]
        )
