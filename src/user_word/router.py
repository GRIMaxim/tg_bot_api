from typing import Any
from fastapi import APIRouter, Depends, BackgroundTasks, status

from .dependencies import get_user_word_db
from .schemas import WordCreateMany, WordDeleteMany, WordReadMany
from .crud import CRUDUserWord
from .constants import RouterPaths

router = APIRouter()


@router.post(RouterPaths.ADD_WORDS, status_code=status.HTTP_202_ACCEPTED)
async def add_list_word(
    user_list_word: WordCreateMany,
    worker: BackgroundTasks,
    user_word_db: CRUDUserWord = Depends(get_user_word_db),
) -> None:
    """Добавление списка слов в бд.

    **Параметры**

    *user_list_word* - схема запроса WordCreateMany.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_word_db* - экземпляр CRUDUserWord для работы с таблицей user_word.
    """
    worker.add_task(user_word_db.add_words, user_list_word)


@router.get(
    RouterPaths.GET_WORDS, status_code=status.HTTP_200_OK, response_model=WordReadMany,
)
async def get_list_word(
    user_id: int,
    user_word_db: CRUDUserWord = Depends(get_user_word_db),
) -> dict[str, Any]:
    """Получение списка слов из бд по user_id.

    **Параметры**

    *user_id* - id пользователя телеграм.

    *user_word_db* - экземпляр CRUDUserWord для работы с таблицей user_word.
    """
    words = await user_word_db.get_words(user_id)
    return {"user_id": user_id, "words": [{"word": data.word, "is_key": data.is_key} for data in words]}


@router.put(RouterPaths.DELETE_WORD_LIST, status_code=status.HTTP_202_ACCEPTED)
async def delete_word_list_by_key(
    user_delete_list_word: WordDeleteMany,
    worker: BackgroundTasks,
    user_word_db: CRUDUserWord = Depends(get_user_word_db),
) -> None:
    """Удаление заданного списка слов из бд по заданной категории.

    **Параметры**

    *user_delete_list_chat* - схема запроса ChatDelete.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_word_db* - экземпляр CRUDUserWord для работы с таблицей user_word.
    """
    worker.add_task(user_word_db.delete_word_list_by_key, user_delete_list_word)


@router.delete(RouterPaths.DELETE_WORDS_BY_KEY, status_code=status.HTTP_202_ACCEPTED)
async def delete_all_words_by_key(
    user_id: int,
    *,
    is_key: bool,
    worker: BackgroundTasks,
    user_word_db: CRUDUserWord = Depends(get_user_word_db),
) -> None:
    """Удаление категории слов пользователя из бд.

    **Параметры**

    *user_id* - id пользователя телеграмм.

    *is_key* - флаг категории слов.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_word_db* - экземпляр CRUDUserWord для работы с таблицей user_word.
    """
    worker.add_task(user_word_db.delete_by_key, user_id, is_key=is_key)
