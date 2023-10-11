from pydantic import BaseModel, ConfigDict


class ChatCreate(BaseModel):
    """Схема запроса на добавление чата."""
    
    user_id: int
    chat_name: str


class ChatCreateMany(BaseModel):
    """Схема запроса на добавление списка чатов."""
    
    chats: list[ChatCreate]


class ChatRead(ChatCreate):
    """Схема запроса на получение чата."""
    
    model_config = ConfigDict(from_attributes=True)


class ChatReadAll(BaseModel):
    """Схема запроса на получение списка чатов."""
    
    chats: list[ChatRead]


class ChatUpdate(ChatCreate):
    """Схема запроса на обновление чата."""


class ChatDelete(ChatCreate):
    """Схема запроса на удаление чата."""


class ChatDeleteMany(ChatCreateMany):
    """Схема запроса на удаление списка чатов."""
