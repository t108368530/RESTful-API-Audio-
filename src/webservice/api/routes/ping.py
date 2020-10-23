from fastapi import APIRouter
from typing import Optional
from webservice.core.config import logger
router = APIRouter()
@router.get("/")
async def get_pong() -> Optional[str]:
    # logger.info()
    return "Pong"