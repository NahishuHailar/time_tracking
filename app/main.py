from fastapi import FastAPI
from app.api.v1.endpoints import project

app = FastAPI()
app.include_router(project.router, prefix="/api/v1")