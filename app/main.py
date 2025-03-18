from app.bootstrap import AppFactory
from app.exceptions import AppError
from app.middleware.error_handler import app_error_handler

app = AppFactory.create_app()

app.add_exception_handler(AppError, app_error_handler)
