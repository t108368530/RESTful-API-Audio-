from fastapi import APIRouter

from webservice.api.routes import ping
from webservice.api.routes.nn import api as nn

router = APIRouter()
router.include_router(ping.router, tags=["ping"], prefix="/ping")
router.include_router(nn.router, tags=["nn"], )

