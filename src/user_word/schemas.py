from pydantic import BaseModel, ConfigDict, Field


class WordCreate(BaseModel):
    """Промежуточная схема для добавления слова."""

    word: str
    is_key: bool


class WordUpdate(WordCreate):
    """Промежуточная схема для обновления слова."""


class WordCreateMany(BaseModel):
    """Схема запроса на добавление списка слов."""

    user_id: int
    words: list[WordCreate] = Field(min_length=1)


class WordReadMany(WordCreateMany):
    """Схема запроса на получение списка слов."""

    model_config = ConfigDict(from_attributes=True)


class WordDeleteMany(BaseModel):
    """Схема запроса на удаление списка слов."""

    is_key: bool
    words: list[str]
    user_id: int
