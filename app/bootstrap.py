from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis.asyncio import Redis

from app.api.v1.endpoits import project, project_user, time_entry, user
from app.cache.backend import RedisBackend
from app.cache.cache import FastAPICache
from app.core.config import RedisSettings


class AppFactoryBase(ABC):
    def __init__(
        self,
        api_prefix: str = "/api/v1",
        cors_origins: list[str] | None = None,
    ) -> None:
        self._api_router = APIRouter(prefix=api_prefix)
        self._cors_origins = cors_origins or []

    async def _lifespan(self, app: FastAPI) -> AsyncGenerator[dict[str, Any], None]:
        redis_settings = RedisSettings.get_settings()
        redis = Redis.from_url(redis_settings.url)
        FastAPICache.init(RedisBackend(redis), prefix="time_tracking", expire=1)

        yield {"redis": redis}

        await redis.close()

    @abstractmethod
    def _setup_api_routers(self, app: FastAPI) -> None:
        raise NotImplementedError

    def _setup_middlewares(self, app: FastAPI) -> None:
        if self._cors_origins:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=self._cors_origins,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )

    def make_app(self) -> FastAPI:
        app = FastAPI(lifespan=asynccontextmanager(self._lifespan))
        self._setup_middlewares(app)
        self._setup_api_routers(app)
        app.include_router(self._api_router)
        return app


class AppFactory(AppFactoryBase):
    def _setup_api_routers(self, app: FastAPI) -> None:
        app.include_router(project.router, prefix="/api/v1")
        app.include_router(user.router, prefix="/api/v1")
        app.include_router(time_entry.router, prefix="/api/v1")
        app.include_router(project_user.router, prefix="/api/v1")

    @classmethod
    def create_app(cls) -> FastAPI:
        factory = cls()
        return factory.make_app()
