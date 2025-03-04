from fastapi import FastAPI
from api.v1.endpoits import project, user,  project_user, time_entry
from exceptions import AppError
from middleware.error_handler import app_error_handler

class AppFactory:

    @staticmethod
    def create_app() -> FastAPI:
        app = FastAPI()

        app.include_router(project.router, prefix="/api/v1")
        app.include_router(user.router, prefix="/api/v1")
        app.include_router(time_entry.router, prefix="/api/v1")
        app.include_router(project_user.router, prefix="/api/v1")

        app.add_exception_handler(AppError, app_error_handler)

        return app
