from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    """Pydantic модель для создания записи о пользователе в бд."""

    user_id: int
    username: str | None = None


class UserUpdate(BaseModel):
    """Pydantic модель для обновления записи о пользователе в бд."""

    user_id: int | None = None
    username: str | None = None
    is_subs_active: bool | None = None
    start_subs_at: datetime | None = None
    end_subs_at: datetime | None = None
    is_trial_used: bool | None = None
    online_search_active: bool | None = None


class UserRead(UserUpdate):
    """Pydantic модель для получения записи о пользователе из бд."""

    create_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserReadAllData(UserRead):
    """Pydantic модель для получения всех данных о пользователе из бд."""

    chats: list[str]


class UserReadAll(BaseModel):
    """Pydantic модель для получения записей о пользователях из бд."""

    users: list[UserRead]
