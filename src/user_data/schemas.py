from datetime import datetime

from pydantic import BaseModel


class CreateUser(BaseModel):
    """."""

    user_id: int
    username: str | None


class UpdateUser(CreateUser):
    """."""

    is_subs_active: bool | None
    start_subs_at: datetime | None
    end_subs_at: datetime | None
    is_trial_used: bool | None
    online_search_active: bool | None
