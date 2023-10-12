from fastapi import FastAPI

from .user_data.router import router as user_router


def get_app() -> FastAPI:
    """Фабрика для создания приложения FastAPI."""
    app = FastAPI()

    app.include_router(user_router)

    return app


main_app = get_app()
