from fastapi import FastAPI

class AppFactory:

    @staticmethod
    def create_app() -> FastAPI:
        app = FastAPI()
        return app
