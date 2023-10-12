from typing import Any
from fastapi import APIRouter, Depends, BackgroundTasks, status

from .dependencies import get_user_chat_db
from .schemas import ChatCreate, ChatDelete, ChatRead
from .crud import CRUDUserChat
from .constants import RouterPaths

router = APIRouter()


@router.post(RouterPaths.ADD_CHATS, status_code=status.HTTP_202_ACCEPTED)
async def add_list_chat(
    user_list_chat: ChatCreate,
    worker: BackgroundTasks,
    user_chat_db: CRUDUserChat = Depends(get_user_chat_db),
) -> None:
    """Добавление списка чатов в бд.

    **Параметры**

    *user_list_chat* - схема запроса ChatCreate.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
    """
    worker.add_task(user_chat_db.add_chats, user_list_chat)


@router.get(RouterPaths.GET_CHATS, status_code=status.HTTP_200_OK, response_model=ChatRead)
async def get_list_chat(
    user_id: int,
    user_chat_db: CRUDUserChat = Depends(get_user_chat_db),
) -> dict[str, Any]:
    """Получение списка чатов из бд по user_id.

    **Параметры**

    *user_id* - id пользователя телеграмм.

    *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
    """
    chats = await user_chat_db.get_chats(user_id)
    return {"user_id": user_id, "chats": chats}


@router.put(RouterPaths.DELETE_CHATS, status_code=status.HTTP_202_ACCEPTED)
async def delete_list_chat(
    user_delete_list_chat: ChatDelete,
    worker: BackgroundTasks,
    user_chat_db: CRUDUserChat = Depends(get_user_chat_db),
) -> None:
    """Удаление заданного списка чатов из бд.

    **Параметры**

    *user_delete_list_chat* - схема запроса ChatDelete.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
    """
    worker.add_task(user_chat_db.delete_chats, user_delete_list_chat)


@router.delete(RouterPaths.DELETE_ALL_CHATS, status_code=status.HTTP_202_ACCEPTED)
async def delete_all_chats(
    user_id: int,
    worker: BackgroundTasks,
    user_chat_db: CRUDUserChat = Depends(get_user_chat_db),
) -> None:
    """Удаление всех чатов пользователя из бд.

    **Параметры**

    *user_id* - id пользователя телеграмм.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_chat_db* - экземпляр CRUDUserChat для работы с таблицей user_chat.
    """
    worker.add_task(user_chat_db.delete_all, user_id)
