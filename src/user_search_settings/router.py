from fastapi import APIRouter, Depends, BackgroundTasks, status

from .dependencies import get_user_search_settings_db
from .schemas import SettingsRead, SettingsUpdate
from .database import UserSearchSettings
from .crud import CRUDUserSearchSettings
from .constants import RouterPaths

router = APIRouter()


@router.get(RouterPaths.GET_SETTINGS, status_code=status.HTTP_200_OK, response_model=SettingsRead)
async def get_user_settings(
    user_id: int,
    user_search_settings_db: CRUDUserSearchSettings = Depends(get_user_search_settings_db),
) -> UserSearchSettings:
    """Получение настроек пользователя для мгновенного поиска.

    **Параметры**

    *user_id* - id пользователя телеграмм.

    *user_search_settings_db* - экземпляр CRUDUserSearchSettings для работы с таблицей user_search_settings.
    """
    return await user_search_settings_db.get_settings_by_user_id(user_id)


@router.put(RouterPaths.UPDATE_SETTINGS, status_code=status.HTTP_202_ACCEPTED)
async def update_user_settings(
    user_settings_update: SettingsUpdate,
    worker: BackgroundTasks,
    user_search_settings_db: CRUDUserSearchSettings = Depends(get_user_search_settings_db),
) -> None:
    """Обновление настроек пользователя для мгновенного поиска.

    **Параметры**

    *user_settings_update* - схема запроса SettingsUpdate.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *user_search_settings_db* - экземпляр CRUDUserSearchSettings для работы с таблицей user_search_settings.
    """
    worker.add_task(user_search_settings_db.update_settings, user_settings_update)
