from fastapi import APIRouter

from webservice.api.routes.nn import cnn_1,mlp_1

router = APIRouter()
router.include_router(cnn_1.router, tags=["cnn_model"], prefix="/nn")
router.include_router(mlp_1.router, tags=["mlp_model"], prefix="/nn")

