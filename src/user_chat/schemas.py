from pydantic import BaseModel, ConfigDict, Field


class ChatCreate(BaseModel):
    """Схема запроса на добавление списка чатов."""

    user_id: int
    chats: list[str] = Field(min_length=1)


class ChatRead(ChatCreate):
    """Схема запроса на получение списка чата."""

    chats: list[str]

    model_config = ConfigDict(from_attributes=True)


class ChatUpdate(ChatCreate):
    """Схема запроса на обновление списка чатов."""


class ChatDelete(ChatCreate):
    """Схема запроса на удаление списка чатов."""
