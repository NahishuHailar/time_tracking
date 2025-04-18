from app.api.v1.endpoits import project, project_user, time_entry, user
from app.bootstrap import AppFactory
from app.exceptions import AppError
from app.middleware.error_handler import app_error_handler

app = AppFactory.create_app()

app.include_router(project.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(time_entry.router, prefix="/api/v1")
app.include_router(project_user.router, prefix="/api/v1")

app.add_exception_handler(AppError, app_error_handler)
