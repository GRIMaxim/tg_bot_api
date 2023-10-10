from fastapi import APIRouter, status, BackgroundTasks

from .crud import CRUDUserData
from .database import UserData
from .exceptions import UserIsAlreadyExist, UserNotFound
from .schemas import UserCreate, UserRead, UserReadAll, UserUpdate
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence

router = APIRouter()


@router.post("/user/", status_code=status.HTTP_202_ACCEPTED, response_model=None)
async def add_user(user_in: UserCreate,
                   worker: BackgroundTasks,
                   user_data_db: CRUDUserData = CRUDUserData(UserData)) -> None: # noqa: B008
    """Добавление пользовательских данных в бд."""
    if await user_data_db.get_by_user_id(user_in.user_id):
        raise UserIsAlreadyExist
    worker.add_task(user_data_db.create, user_in)


@router.get("/user/", status_code=status.HTTP_200_OK, response_model=UserRead)
async def get_user(user_id: int | None = None,
                   username: str | None = None,
                   user_data_db: CRUDUserData = CRUDUserData(UserData)) -> UserData: # noqa: B008
    """Получение пользовательских данных из бд."""
    user_out: UserData | None = None
    if user_id:
        user_out = await user_data_db.get_by_user_id(user_id)
    if username:
        user_out = await user_data_db.get_by_username(username)
    if not user_out:
        raise UserNotFound
    return user_out


@router.get("/user/all", status_code=status.HTTP_200_OK, response_model=UserReadAll)
async def get_users(offset: int = 1,
                    limit: int = 100,
                    user_data_db: CRUDUserData = CRUDUserData(UserData)) -> dict[str, list[UserRead]]: # noqa: B008
    """Получение списка всех пользовательских данных из бд."""
    users: Sequence[UserData] = await user_data_db.get_all(offset=offset, limit=limit)
    return {"users": [UserRead.model_validate(user) for user in users]}


@router.put("/user/", status_code=status.HTTP_202_ACCEPTED, response_model=None)
async def update_user(user_update: UserUpdate,
                      worker: BackgroundTasks,
                      user_data_db: CRUDUserData = CRUDUserData(UserData)) -> None: # noqa: B008
    """Обновление заданных полей пользователя в бд."""
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
