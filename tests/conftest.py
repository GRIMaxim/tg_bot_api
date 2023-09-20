import asyncio
from asyncio import AbstractEventLoop
from collections.abc import Iterator

import pytest


@pytest.fixture(autouse=True, scope="session")
def _run_migrations() -> Iterator[None]:
    """Запуск миграций для тестовой базы данных и дальнейшее их удаление."""
    from pathlib import Path

    from alembic.config import Config
    from alembic import command

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    revision = command.revision(
        alembic_cfg, message="test_table_init", autogenerate=True
    )
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "-1")

    if revision is not None:
        if isinstance(revision, list):
            for rev in revision:
                if rev:
                    Path(rev.path).unlink()
        else:
            Path(revision.path).unlink()


@pytest.fixture(autouse=True, scope="session")
def event_loop() -> Iterator[AbstractEventLoop]:
    """Получение цикла событий."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
