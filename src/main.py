from fastapi import FastAPI

from .user_data.router import router as user_router


def get_app() -> FastAPI:
    """."""
    app = FastAPI(root_path="/api/v1/")

    app.include_router(user_router)

    return app


main_app = get_app()
