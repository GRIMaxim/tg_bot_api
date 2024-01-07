from src.crud import CRUDBase

from .database import Subscription
from .schemas import SubscriptionCreate, SubscriptionUpdate


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    """Методы CRUD для работы с таблицей subscription."""
