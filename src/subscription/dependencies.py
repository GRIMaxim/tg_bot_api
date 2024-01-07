from .database import Subscription
from .crud import CRUDSubscription


def get_subscription_db() -> CRUDSubscription:
    """Фабрика для получения экземпляра CRUDSubscription."""
    return CRUDSubscription(Subscription)
