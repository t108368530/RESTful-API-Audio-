from fastapi import APIRouter, UploadFile, File
from fastapi.responses import UJSONResponse
from typing import Optional

from webservice.core.config import message_queue2, settings
from webservice.utils.preprocessor import make_spec
import base64
import uuid
import ujson
import io

router = APIRouter()
@router.post("/ctc_1", response_class=UJSONResponse)
async def get_res_predict(
    input_data: UploadFile = File(...),
) -> Optional[UJSONResponse]:
    # X = input_data.file
    # data = io.BytesIO(input_data)
    if (input_data.content_type == "audio/wav" or input_data.content_type == "audio/x-wav"):
        await input_data.seek(0)
        input_data = await input_data.read()
        ##  In memory temporary file
        with io.BytesIO() as mem_temp_file:
            mem_temp_file.write(input_data)
            mem_temp_file.seek(0)
            # print(mem_temp_file) 
            data = make_spec(mem_temp_file)
            data = base64.b64encode(data).decode("utf-8")
            # print(data)
            ID = str(uuid.uuid4())
            Q_DATA = {"id": ID, "audio_feature": data}
            message_queue2.rpush(settings.QUEUE_NAME_2, ujson.dumps(Q_DATA))

        sub=message_queue2.pubsub()
        sub.subscribe(ID)
        for mes in sub.listen():
            responses=mes.get('data')
            if isinstance(responses, bytes):
                res=responses.decode('utf-8')
                res=ujson.loads(res)
                del sub
                break
        return res
    else:
        return {"Error": "Type Error"}