from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Pydantic модель для создания записи о пользователе в бд."""

    user_id: int
    username: str | None


class UserUpdate(UserCreate):
    """Pydantic модель для обновления записи о пользователе в бд."""

    is_subs_active: bool | None
    start_subs_at: datetime | None
    end_subs_at: datetime | None
    is_trial_used: bool | None
    online_search_active: bool | None


class UserRead(UserUpdate):
    """."""

    create_at: datetime


class UserReadAll(BaseModel):
    """."""

    users: list[UserRead]
