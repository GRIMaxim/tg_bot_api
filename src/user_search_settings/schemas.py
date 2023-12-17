from pydantic import BaseModel, ConfigDict, Field


class SettingsCreate(BaseModel):
    """Промежуточная схема для добавления настроек."""

    user_id: int
    start_date: str
    end_date: bool


class SettingsUpdate(SettingsCreate):
    """Промежуточная схема для обновления настроек."""


class SettingsRead(SettingsCreate):
    """Схема запроса на получение настроек пользователя."""

    model_config = ConfigDict(from_attributes=True)
