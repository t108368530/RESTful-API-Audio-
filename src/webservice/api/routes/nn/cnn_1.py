from fastapi import APIRouter, UploadFile, File
from fastapi.responses import UJSONResponse
from typing import Optional

from webservice.core.config import message_queue, settings
from webservice.utils.preprocessor import extract_Features
import base64
import uuid
import ujson
import io


router = APIRouter()


@router.post("/cnn_1", response_class=UJSONResponse)
async def get_res_predict(
    input_data: UploadFile = File(...),
) -> Optional[UJSONResponse]:
    # X = input_data.file
    # data = io.BytesIO(input_data)
    if input_data.content_type == "audio/wave":
        await input_data.seek(0)
        input_data = await input_data.read()
        ##  In memory temporary file
        with io.BytesIO() as mem_temp_file:
            mem_temp_file.write(input_data)
            mem_temp_file.seek(0)
            data = extract_Features(mem_temp_file)
            data = base64.b64encode(data).decode("utf-8")
            ID = str(uuid.uuid4())
            Q_DATA = {"id": ID, "audio_feature": data}
            message_queue.rpush(settings.QUEUE_NAME, ujson.dumps(Q_DATA))
        QUIT_COUNT=0
        while QUIT_COUNT<1000:
            QUIT_COUNT+=1
            res = message_queue.get(ID)
            if res != None:
                res = res.decode('utf-8')
                message_queue.delete(ID)
                res=ujson.loads(res)
                res["res"]=int(res["res"])
                break

        return res
    else:
        return {"Error": "Content Type Error"}
