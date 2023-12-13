from typing import Any
from collections.abc import Mapping, Sequence

from sqlalchemy import insert, delete, select, Row
from pydantic import BaseModel

from src.crud import CRUDBase
from src.utils import async_execute

from .database import UserWord
from .schemas import (
    WordCreate,
    WordUpdate,
    WordCreateMany,
    WordDeleteMany,
)


class CRUDUserWord(CRUDBase[UserWord, WordCreate, WordUpdate]):
    """Методы CRUD для работы с таблицей user_word."""

    async def add_words(self, user_words: WordCreateMany | Mapping[str, Any]) -> None:
        """Добавление списка слов в базу данных.

        **Параметры**

        *user_words* - схема запроса на добавление списка слов
        с обязательными полями 'user_id'(id пользователя telegram)
        и 'word_list' (список словарей с полями word и is_key).
        """
        if isinstance(user_words, BaseModel):
            user_words = user_words.model_dump()

        word_list = [
            {
                "user_id": user_words["user_id"],
                "word": word_dict["word"],
                "is_key": word_dict["is_key"],
            }
            for word_dict in user_words["words"]
        ]

        query = insert(self.model).values(word_list)
        await async_execute(query)

    async def get_words(self, user_id: int) -> Sequence[UserWord]:
        """Получение списка слов из базы данных.

        **Параметры**

        *user_id* - id пользователя telegram.
        """
        query = select(self.model).where(self.model.user_id == user_id)
        result = await async_execute(query)
        return result.scalars().all()

    async def delete_word_list_by_key(
        self,
        words_for_delete: WordDeleteMany | Mapping[str, Any],
    ) -> None:
        """Удаляет заданную категорию слов из бд.

        **Параметры**

        *words_for_delete* - схема запроса на удаление списка слов
        с обязательными полями 'user_id' и 'words'.
        """
        if isinstance(words_for_delete, BaseModel):
            words_for_delete = words_for_delete.model_dump()

        query = delete(self.model).where(
            (self.model.user_id == words_for_delete["user_id"])
            & (self.model.word.in_(words_for_delete["words"]))
            & (self.model.is_key == words_for_delete["is_key"]),
        )
        await async_execute(query)

    async def delete_by_key(self, user_id: int, is_key: bool) -> None:
        """Удаляет все слова из бд по ключу is_key.

        **Параметры**

        *user_id* - id пользователя telegram.
        *is_key*  - ключ для определения группы слов.
        """
        query = delete(self.model).where((self.model.user_id == user_id) & (self.model.is_key == is_key))
        await async_execute(query)
