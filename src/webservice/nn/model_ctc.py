from webservice.core.config import message_queue2, settings
import ujson
import base64
import numpy as np
from tensorflow.keras.layers import *
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import Add
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras import backend as K
from tensorflow.keras.utils import plot_model
import ujson
import os
from time import sleep

char_map_str = """
<SPACE> 0
a 1
b 2
c 3
d 4
e 5
f 6
g 7
h 8
i 9
j 10
k 11
l 12
m 13
n 14
o 15
p 16
q 17
r 18
s 19
t 20
u 21
v 22
w 23
x 24
y 25
z 26
' 27

"""

char_map = {}
index_map = {}

for line in char_map_str.strip().split("\n"):
    ch, index = line.split()
    char_map[ch] = int(index)
    index_map[int(index)] = ch

index_map[0] = " "

def ctc_lambda_func(args):
    y_pred, labels, input_length, label_length = args    
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)    


def ctc(y_true, y_pred):
    return y_pred

class CTC:
    """
    Usage:
        sr_ctc = CTC(enter input_size and output_size)
        sr_ctc.build()
        sr_ctc.m.compile()
        sr_ctc.tm.compile()
    """

    def __init__(self, input_size=None, output_size=None, initializer="glorot_uniform"):
        self.input_size = input_size
        self.output_size = output_size
        self.initializer = initializer
        self.m = None
        self.tm = None

    def build(
        self,
        conv_filters=196,
        conv_size=13,
        conv_strides=4,
        act="relu",
        rnn_layers=2,
        LSTM_units=128,
        drop_out=0.8,
    ):
        print(self.input_size)
        i = Input(shape=self.input_size, name="input")
        x = Conv1D(
            conv_filters,
            conv_size,
            strides=conv_strides,
            name="conv1d",
            input_shape=self.input_size,
        )(i)
        x = BatchNormalization()(x)
        x = Activation(act)(x)
        for _ in range(rnn_layers):
            x = Bidirectional(LSTM(LSTM_units, return_sequences=True))(x)
            x = Dropout(drop_out)(x)
            x = BatchNormalization()(x)
        y_pred = TimeDistributed(Dense(self.output_size, activation="softmax"))(x)
        # ctc inputs
        labels = Input(
            name="the_labels",
            shape=[
                None,
            ],
            dtype="int32",
        )
        input_length = Input(name="input_length", shape=[1], dtype="int32")
        label_length = Input(name="label_length", shape=[1], dtype="int32")
        loss_out = Lambda(ctc_lambda_func, output_shape=(1,), name="ctc")(
            [y_pred, labels, input_length, label_length]
        )
        self.tm = Model(inputs=i, outputs=y_pred)
        self.m = Model(inputs=[i, labels, input_length, label_length], outputs=loss_out)
        return self.m, self.tm





# def load_model():
# 	sr_ctc = CTC((122,85), 28)
# 	sr_ctc.build()
# 	sr_ctc.m.compile(loss=ctc, optimizer="adam", metrics=["accuracy"])
# 	sr_ctc.tm.compile(loss=ctc, optimizer="adam")
# 	sr_ctc.tm.load_weights("/home/alien/webservice/src/webservice/nn_model/ctc.h5")
#     return sr_ctc


def classify_process():
	os.environ["CUDA_VISIBLE_DEVICES"] = "1"
	model = CTC((122,85), 28)
	model.build()
	model.m.compile(loss=ctc, optimizer="adam", metrics=["accuracy"])
	model.tm.compile(loss=ctc, optimizer="adam")
	model.tm.load_weights("/home/alien/webservice/src/webservice/nn_model/ctc.h5")
	while True:
		if message_queue2.llen(settings.QUEUE_NAME_2) != 0:
			q = ujson.loads(message_queue2.lpop(settings.QUEUE_NAME_2).decode("utf-8"))
			feature = bytes(q["audio_feature"], encoding="utf-8")
			ID = q["id"]
			feature = np.frombuffer(base64.decodebytes(feature),dtype=np.float32)
			# print(feature)
			# print(np.array(feature.reshape(), dtype=np.float32).shape)
			k_ctc_out = K.ctc_decode(model.tm.predict(np.expand_dims(np.squeeze(feature.reshape(122,85)),axis=0), verbose=0),np.array([28]))
			decoded_out = K.eval(k_ctc_out[0][0])
			str_decoded_out = []
			for i, _ in enumerate(decoded_out):
				str_decoded_out.append("".join([index_map[c] for c in decoded_out[i] if not c == -1]))
			# print(str_decoded_out)
			message_queue2.set(ID, ujson.dumps({"res": str_decoded_out[0]}))
			message_queue2.publish(ID, ujson.dumps({"res": str_decoded_out[0]}))

            # 	yp=np.argmax(model.predict(feature.reshape(1, 277, 1)))

if __name__ == "__main__":
	classify_process()
