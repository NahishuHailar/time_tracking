from exceptions import AppError
from fastapi import Request
from fastapi.responses import JSONResponse


async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
