from typing import TYPE_CHECKING

from fastapi import APIRouter, status, BackgroundTasks, Depends

from .crud import CRUDUserData
from .database import UserData
from .exceptions import UserIsAlreadyExist, UserNotFound
from .schemas import UserCreate, UserRead, UserReadAll, UserUpdate, UserReadAllData
from .dependencies import get_user_data_db
from .constants import RouterPaths

if TYPE_CHECKING:
    from collections.abc import Sequence


router = APIRouter()


@router.post(
    RouterPaths.CREATE_USER, status_code=status.HTTP_202_ACCEPTED, response_model=None,
)
async def add_user(
    user_in: UserCreate,
    worker: BackgroundTasks,
    user_data_db: CRUDUserData = Depends(get_user_data_db),
) -> None:
    """Добавление пользовательских данных в бд.

    **Параметры**

    *user_in* - схема запроса UserCreate.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_data_db* - экземпляр CRUDUserData для работы с базой данных.
    """
    if await user_data_db.get_by_user_id(user_in.user_id):
        raise UserIsAlreadyExist
    worker.add_task(user_data_db.create, user_in)


@router.get(
    RouterPaths.GET_USER, status_code=status.HTTP_200_OK, response_model=UserRead,
)
async def get_user(
    user_id: int | None = None,
    username: str | None = None,
    user_data_db: CRUDUserData = Depends(get_user_data_db),
) -> UserData:
    """Получение пользовательских данных из бд.

    **Параметры**

    *user_id* - id пользователя telegram.

    *username* - username пользователя telegram.

    *user_data_db* - экземпляр CRUDUserData для работы с базой данных.
    """
    user_out: UserData | None = None
    if user_id:
        user_out = await user_data_db.get_by_user_id(user_id)
    if username:
        user_out = await user_data_db.get_by_username(username)
    if not user_out:
        raise UserNotFound
    return user_out


@router.get(
    RouterPaths.GET_ALL_USER_DATA,
    status_code=status.HTTP_200_OK,
    response_model=UserReadAllData,
)
async def get_all_user_data(
    user_id: int | None = None,
    user_data_db: CRUDUserData = Depends(get_user_data_db),
) -> UserData:
    """Получение пользовательских данных из всех связанных таблиц.

    **Параметры**

    *user_id* - id пользователя telegram.

    *user_data_db* - экземпляр CRUDUserData для работы с базой данных.
    """
    user_out: UserData | None = None
    if user_id:
        user_out = await user_data_db.get_by_user_id_with_fk(user_id)
    if not user_out:
        raise UserNotFound
    return user_out


@router.get(
    RouterPaths.GET_ALL_USERS,
    status_code=status.HTTP_200_OK,
    response_model=UserReadAll,
)
async def get_users(
    offset: int = 1,
    limit: int = 100,
    user_data_db: CRUDUserData = Depends(get_user_data_db),
) -> dict[str, list[UserRead]]:
    """Получение списка всех пользовательских данных из бд.

    **Параметры**

    *offset* - с какого pk начать получение записей, по умолчанию 0 (аналог OFFSET из SQL).

    *limit* - ограничение на получение числа записей, по умолчанию 100 записей (аналог LIMIT из SQL).

    *user_data_db* - экземпляр CRUDUserData для работы с базой данных.
    """
    users: Sequence[UserData] = await user_data_db.get_all(offset=offset, limit=limit)
    return {"users": [UserRead.model_validate(user) for user in users]}


@router.put(
    RouterPaths.UPDATE_USER, status_code=status.HTTP_202_ACCEPTED, response_model=None,
)
async def update_user(
    user_update: UserUpdate,
    worker: BackgroundTasks,
    user_data_db: CRUDUserData = Depends(get_user_data_db),
) -> None:
    """Обновление заданных полей пользователя в бд.

    **Параметры**

    *user_update* - схема запроса UserUpdate.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_data_db* - экземпляр CRUDUserData для работы с базой данных.
    """
    user_for_update = user_update.model_dump()

    user_id = user_for_update.get("user_id")
    username = user_for_update.get("username")

    user: UserData | None = None
    if user_id:
        user = await user_data_db.get_by_user_id(user_id)
    if username:
        user = await user_data_db.get_by_username(username)
    if not user:
        raise UserNotFound

    worker.add_task(user_data_db.update, user_update)
