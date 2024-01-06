from fastapi import FastAPI

from .user_data.router import router as user_router
from .user_chat.router import router as user_chat_router
from .user_word.router import router as user_word_router
from .user_search_settings.router import router as settings_router


def get_app() -> FastAPI:
    """Фабрика для создания приложения FastAPI."""
    app = FastAPI()

    app.include_router(user_router)
    app.include_router(user_chat_router)
    app.include_router(user_word_router)
    app.include_router(settings_router)

    return app


main_app = get_app()
