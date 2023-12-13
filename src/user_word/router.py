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
    """Добавление списка чатов в бд.

    **Параметры**

    *user_list_word* - схема запроса ChatCreate.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
    """
    worker.add_task(user_word_db.add_words, user_list_word)


@router.get(
    RouterPaths.GET_WORDS, status_code=status.HTTP_200_OK, response_model=WordReadMany
)
async def get_list_word(
    user_id: int,
    user_word_db: CRUDUserWord = Depends(get_user_word_db),
) -> dict[str, Any]:
    """Получение списка чатов из бд по user_id.

    **Параметры**

    *user_id* - id пользователя телеграмм.

    *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
    """
    words = await user_word_db.get_words(user_id)
    return {"user_id": user_id, "words": [{"word": data.word, "is_key": data.is_key} for data in words]}


# @router.put(RouterPaths.DELETE_CHATS, status_code=status.HTTP_202_ACCEPTED)
# async def delete_list_chat(
#     user_delete_list_chat: ChatDelete,
#     worker: BackgroundTasks,
#     user_chat_db: CRUDUserChat = Depends(get_user_chat_db),
# ) -> None:
#     """Удаление заданного списка чатов из бд.
#
#     **Параметры**
#
#     *user_delete_list_chat* - схема запроса ChatDelete.
#
#     *worker* - BackgroundTasks для выполнения задач в фоне.
#
#     *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
#     """
#     worker.add_task(user_chat_db.delete_chats, user_delete_list_chat)
#
#
# @router.delete(RouterPaths.DELETE_ALL_CHATS, status_code=status.HTTP_202_ACCEPTED)
# async def delete_all_chats(
#     user_id: int,
#     worker: BackgroundTasks,
#     user_chat_db: CRUDUserChat = Depends(get_user_chat_db),
# ) -> None:
#     """Удаление всех чатов пользователя из бд.
#
#     **Параметры**
#
#     *user_id* - id пользователя телеграмм.
#
#     *worker* - BackgroundTasks для выполнения задач в фоне.
#
#     *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
#     """
#     worker.add_task(user_chat_db.delete_all, user_id)
