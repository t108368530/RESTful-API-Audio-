from webservice.core.config import message_queue,settings
import ujson
import base64
import numpy as np
import tensorflow as tf
import ujson
import os 
from time import sleep
def load_model():
	with open('/home/alien/webservice/src/webservice/nn_model/model_2.json','r') as jsonf:
		model=tf.keras.models.model_from_json(jsonf.read())
		model.load_weights('/home/alien/webservice/src/webservice/nn_model/model_2.h5')
		return model


def classify_process():
	os.environ["CUDA_VISIBLE_DEVICES"] = "1"
	model=load_model()
	while True:
		if message_queue.llen(settings.QUEUE_NAME) != 0:
			q = ujson.loads(message_queue.lpop(settings.QUEUE_NAME).decode("utf-8"))
			feature = bytes(q["audio_feature"], encoding="utf-8")
			ID = q["id"]
			feature = np.frombuffer(base64.decodebytes(feature),dtype=np.float)
			yp=np.argmax(model.predict(feature.reshape(1, 277, 1)))
			message_queue.set(ID, ujson.dumps({"res": str(yp)}))

		
if __name__ == "__main__":
	classify_process()