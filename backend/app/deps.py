from typing import Iterator

from sqlmodel import Session

from .db import engine
from .websocket_manager import ConnectionManager


manager = ConnectionManager()


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_ws_manager():
    return manager


