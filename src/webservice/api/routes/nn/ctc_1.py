from fastapi import APIRouter, UploadFile, File
from fastapi.responses import UJSONResponse
from typing import Optional

from webservice.core.config import message_queue2, settings
from webservice.utils.preprocessor import make_spec
from pydub import AudioSegment
import base64
import uuid
import ujson
import io
import soundfile as sf
import time


router = APIRouter()


@router.post("/ctc_1", response_class=UJSONResponse)
async def get_res_predict(
    input_data: UploadFile = File(...),
) -> Optional[UJSONResponse]:
    # X = input_data.file
    # data = io.BytesIO(input_data)
    if (
        input_data.content_type == "audio/wav"
        or input_data.content_type == "audio/x-wav"
    ):
        ID = str(uuid.uuid4())
        sub = message_queue2.pubsub()
        sub.subscribe(ID)
        # input_data.seek(0)
        # input_data = await input_data.read()
        
        
        for mes in sub.listen():
            responses = mes.get("data")
            if isinstance(responses, bytes):
                res = responses.decode("utf-8")
                res = ujson.loads(res)
                break
            elif responses == 1:
                await input_data.seek(0)
                input_data = await input_data.read()
                with io.BytesIO() as mem_temp_file:
                    mem_temp_file.write(input_data)
                    mem_temp_file.seek(0)
                    # AudioSegment.from_file(mem_temp_file).export(f"{time.time()}.wav","wav")
                    # # temp=mem_temp_file
                    # data, samplerate = sf.read(mem_temp_file)
                    # sf.write(f'{time.time()}.wav', data, samplerate)
                    data = make_spec(mem_temp_file)
                    data = base64.b64encode(data).decode("utf-8")
                    Q_DATA = {"id": ID, "audio_feature": data}
                    message_queue2.rpush(settings.QUEUE_NAME_2, ujson.dumps(Q_DATA))

        message_queue2.close()
        sub.close()
        return res
    else:
        return {"Error": "Type Error"}
