"""Application factory. `app` is the module-level instance the drift test imports."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from miniflow import __version__
from miniflow.db import Base, engine
from miniflow.routers import auth, events, people


@asynccontextmanager
async def _lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


def create_app() -> FastAPI:
    application = FastAPI(title="mini-flow", version=__version__, lifespan=_lifespan)
    application.include_router(auth.router)
    application.include_router(people.router)
    application.include_router(events.router)

    @application.get("/health", tags=["ops"])
    def health_check() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    return application


app = create_app()
