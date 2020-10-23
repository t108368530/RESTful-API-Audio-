from fastapi import FastAPI

from webservice.api.routes.api import router as api_router
from webservice.core.config import settings


def get_application() -> FastAPI:
    application = FastAPI(title="RESTful API", debug=True)
    application.include_router(api_router, prefix="/api")
    return application


app = get_application()
