from fastapi import APIRouter
from fastapi.responses import UJSONResponse
from typing import Optional

router = APIRouter()
@router.post("/mlp_1", response_class=UJSONResponse)
async def get_res_predict() -> Optional[UJSONResponse]:
    return {"mlp_model": "mm"}