from fastapi import APIRouter
from typing import Optional
from webservice.core.config import logger
from fastapi.responses import UJSONResponse

router = APIRouter()
@router.get("/")
async def get_pong() -> Optional[UJSONResponse]:
    # logger.info()
    return {"ping":"PONG!"}