from fastapi import APIRouter

from webservice.api.routes.nn import cnn_1,ctc_1

router = APIRouter()
router.include_router(cnn_1.router, tags=["cnn_model"], prefix="/nn")
router.include_router(ctc_1.router, tags=["ctc_model"], prefix="/nn")

