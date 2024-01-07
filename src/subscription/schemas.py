from pydantic import BaseModel, ConfigDict


class SubscriptionCreate(BaseModel):
    """Схема запроса для добавления подписки и ее настроек."""

    subscription_name: str | None
    duration: int | None
    chat_limit: int | None
    word_limit: int | None
    is_visible: bool | None


class SubscriptionUpdate(SubscriptionCreate):
    """Схема запроса для обновления подписки и ее настроек."""

    pk: int


class SubscriptionRead(SubscriptionCreate):
    """Схема для получения подписки и ее настроек."""

    model_config = ConfigDict(from_attributes=True)


class SubscriptionReadMany(BaseModel):
    """Схема для получения списка подписок."""

    subscription_list: list[SubscriptionRead]
