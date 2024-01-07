from collections.abc import Sequence
from fastapi import APIRouter, Depends, BackgroundTasks, status

from .dependencies import get_subscription_db
from .database import Subscription
from .schemas import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionRead,
    SubscriptionReadMany,
)
from .crud import CRUDSubscription
from .constants import RouterPaths

router = APIRouter()


@router.post(RouterPaths.CREATE_SUBSCRIPTION, status_code=status.HTTP_202_ACCEPTED)
async def add_subscription(
    subscription_data: SubscriptionCreate,
    worker: BackgroundTasks,
    subscription_db: CRUDSubscription = Depends(get_subscription_db),
) -> None:
    """Добавление подписки в бд.

    **Параметры**

    *subscription_data* - схема запроса SubscriptionCreate.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *subscription_db* - экземпляр CRUDSubscription для работы с таблицей subscription.
    """
    worker.add_task(subscription_db.create, subscription_data)


@router.get(
    RouterPaths.GET_SUBSCRIPTION,
    status_code=status.HTTP_200_OK,
    response_model=SubscriptionRead,
)
async def get_subscription_by_pk(
    pk: int,
    subscription_db: CRUDSubscription = Depends(get_subscription_db),
) -> Subscription:
    """Получение подписки из бд по pk.

    **Параметры**

    *pk* - порядковый номер подписки.

    *subscription_db* - экземпляр CRUDSubscription для работы с таблицей subscription.
    """
    return await subscription_db.get(pk)


@router.get(
    RouterPaths.GET_SUBSCRIPTIONS,
    status_code=status.HTTP_200_OK,
    response_model=SubscriptionReadMany,
)
async def get_subscriptions(
    offset: int | None,
    limit: int | None,
    subscription_db: CRUDSubscription = Depends(get_subscription_db),
) -> list[SubscriptionRead]:
    """Получение списка подпискок из бд.

    **Параметры**

    *subscription_db* - экземпляр CRUDSubscription для работы с таблицей subscription.
    """
    subscriptions = await subscription_db.get_all(offset=offset, limit=limit)
    return [SubscriptionRead.model_validate(sub) for sub in subscriptions]


@router.put(RouterPaths.UPDATE_SUBSCRIPTION, status_code=status.HTTP_202_ACCEPTED)
async def update_subscription(
    subscription_update: SubscriptionUpdate,
    worker: BackgroundTasks,
    subscription_db: CRUDSubscription = Depends(get_subscription_db),
) -> None:
    """Обновление данных подписки.

    **Параметры**

    *subscription_update* - схема запроса SubscriptionUpdate.

    *worker* - BackgroundTasks для выполнения задач в фоне.

    *subscription_db* - экземпляр CRUDSubscription для работы с таблицей subscription.
    """
    worker.add_task(subscription_db.update, subscription_update)
