from typing import Any, ClassVar

from faker import Faker

from src.user_data.crud import CRUDUserData
from src.user_word.crud import CRUDUserWord
from src.user_word.schemas import WordCreateMany, WordCreate, WordDeleteMany

fk = Faker()


class TestCRUDUserWords:
    """Сборка тестов для CRUDUserWords."""

    user: ClassVar[dict[str, Any]] = {"user_id": fk.random_int(), "username": fk.name()}
    word_data: ClassVar[WordCreateMany] = WordCreateMany(
        user_id=user["user_id"],
        words=[WordCreate(word=fk.name(), is_key=i % 2 == 0) for i in range(100)],
    )

    async def test_create_get(
        self,
        user_data_db: CRUDUserData,
        user_word_db: CRUDUserWord,
    ) -> None:
        """Тестирование CRUDUserWords.add_words и CRUDUserWords.get_words."""
        await user_data_db.create(self.user)
        await user_word_db.add_words(self.word_data)
        db_words = await user_word_db.get_words(self.user["user_id"])
        assert {(el.word, el.is_key) for el in db_words} == {
            (data.word, data.is_key) for data in self.word_data.words
        }

    async def test_delete_keys(
        self,
        user_word_db: CRUDUserWord,
    ) -> None:
        """Тестирование CRUDUserWords.delete_by_key для удаления некоторых ключевых слов."""
        words_for_delete = [
            words.word for words in self.word_data.words[:10] if words.is_key
        ]
        in_data = WordDeleteMany(
            user_id=self.user["user_id"], words=words_for_delete, is_key=True
        )
        await user_word_db.delete_word_list_by_key(in_data)
        db_words = await user_word_db.get_words(self.user["user_id"])
        assert {(el.word, el.is_key) for el in db_words if el.is_key} == {
            (data.word, data.is_key)
            for data in self.word_data.words[10:]
            if data.is_key
        }

    async def test_delete_excepts(
        self,
        user_word_db: CRUDUserWord,
    ) -> None:
        """Тестирование CRUDUserWords.delete_by_key для удаления некоторых исключающих слов."""
        words_for_delete = [
            words.word for words in self.word_data.words[:10] if not words.is_key
        ]
        in_data = WordDeleteMany(
            user_id=self.user["user_id"], words=words_for_delete, is_key=False
        )
        await user_word_db.delete_word_list_by_key(in_data)
        db_words = await user_word_db.get_words(self.user["user_id"])
        assert {(el.word, el.is_key) for el in db_words if not el.is_key} == {
            (data.word, data.is_key)
            for data in self.word_data.words[10:]
            if not data.is_key
        }

    async def test_delete_all_keys(
        self,
        user_word_db: CRUDUserWord,
    ) -> None:
        """Тестирование CRUDUserWords.delete_by_key для удаления только ключевых слов."""
        await user_word_db.delete_by_key(self.user["user_id"], is_key=True)
        db_words = await user_word_db.get_words(self.user["user_id"])
        assert not all(el.is_key for el in db_words)

    async def test_delete_all_excepts(
        self,
        user_word_db: CRUDUserWord,
    ) -> None:
        """Тестирование CRUDUserWords.delete_by_key для удаления только исключающих слов."""
        await user_word_db.delete_by_key(self.user["user_id"], is_key=False)
        db_words = await user_word_db.get_words(self.user["user_id"])
        assert not db_words
