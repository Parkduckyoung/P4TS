from keras.preprocessing import sequence
from keras.models import Model, Sequential
from keras.layers import Dense, Flatten, Dropout, LSTM, Input, Embedding, Conv1D, MaxPooling1D, Activation
from keras.optimizers import SGD,Adam
import keras.layers as layers
import numpy as np
import json
import data_set as ds
from keras.utils import to_categorical
import tensorflow as tf
from keras_multi_head import MultiHeadAttention, MultiHead
from keras_self_attention import SeqSelfAttention
import keras
import nltk

from keras.layers import Activation
from keras.utils.generic_utils import get_custom_objects

def custom_gelu(x):
    return 0.5 * x * (1 + tf.tanh(tf.sqrt(2 / np.pi) * (x + 0.044715 * tf.pow(x, 3))))
get_custom_objects().update({'custom_gelu': Activation(custom_gelu)})

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
company = '한일현대엘리베이'

data = ds.data_set(300,company,'2010.06.05','2019.05.31','2019.06.01','2019.12.31')

train_docs,test_docs = data.docs_data()
"""
tokens = [t for d in train_docs for t in d[0]]
text = nltk.Text(tokens,name='NMSC')

print(len(text.tokens))
print(len(set(text.tokens)))

selected_words = [f[0] for f in text.vocab().most_common(100)]

with open('stopword.json',"r",encoding='utf-8') as f:
        selected_words = json.load(f)
"""

wv = ds.word_vector(300)
train_x,train_y = wv.Convert2Vec('Word2vec',train_docs)
test_x, test_y = wv.Convert2Vec('Word2vec',test_docs)

train_seq_length = [len(x) for x in train_x]
test_seq_length = [len(x) for x in test_x]
Maxseq_length = max(train_seq_length)
if Maxseq_length < max(test_seq_length):
    Maxseq_length = max(test_seq_length)
print(Maxseq_length)
index = int(len(train_x)/2)
train_x = wv.Zero_padding(train_x,Maxseq_length)
test_x = wv.Zero_padding(test_x,Maxseq_length)

#train_y = to_categorical(train_y)
#test_y = to_categorical(test_y)
model = Sequential()

model.add(Conv1D(32,
                 3,
                 padding='valid',
                 activation='custom_gelu',
                 strides=1))
model.add(MaxPooling1D(pool_size=2))

model.add(MultiHeadAttention(
    head_num=32,
    name='Multi-Head-Attention',
))
model.add(layers.LSTM(32,return_sequences=True))
model.add(layers.Flatten())
model.add(Dropout(0.5))
model.add(layers.Dense(1,activation='sigmoid'))
model.build()
model.summary
model.compile(optimizer=Adam(lr=0.001),loss=keras.losses.binary_crossentropy,metrics=['accuracy'])
model.fit(train_x, train_y, batch_size=64,epochs=60)
scores = model.evaluate(test_x, test_y, verbose=2)

print("Accuracy: %.2f%%" % (scores[1]*100))
"""
text = layers.Conv2D(64,(3,300),padding='valid',strides = 1)(news_input)
text1 = layers.MaxPooling2D(pool_size = (1,1))(text)

text = layers.Conv2D(64,(4,300),padding='valid',strides = 1)(news_input)
text2 = layers.MaxPooling2D(pool_size = (2,2))(text)

text = layers.Conv2D(64,(5,300),padding='valid',strides = 1)(news_input)
text3 = layers.MaxPooling2D(pool_size = (2,2))(text)


text = layers.concatenate([text1, text2, text3])
#sess = tf.Session()
#sess.run(tf.global_variables_initializer())
#text = tf.reshape(text,shape=[-1,3]).eval(session=sess)
print(text)


news_input = Input(shape=(16,300),dtype='float32')
#text = Embedding(input_dim=16,output_dim=300,
#                   mask_zero=True)(news_input)
text =SeqSelfAttention(attention_activation='relu')(news_input)
text = layers.Flatten(name='Flatten')(text)
text =layers.LSTM(128)(text)
text =layers.Dense(128,activation='relu')(text)
text = Dropout(0.5)(text)



# 연결합니다.
#concatenated = layers.concatenate([text, tech],axis=0)

# softmax 분류기를 추가합니다.
answer = layers.Dense(1, activation='sigmoid')(text)
# 모델 객체를 만들고 2개의 입력과 출력을 주입합니다.
#model = Model(input = [news_input, technical_input], output = answer)
model = Model(input = news_input, output = answer)

model.compile(optimizer=Adam(lr=0.1),
               loss='categorical_crossentropy',
               metricss=['accuracy'])

history_bidir_atom = model.fit(train_x, train_y,
                    batch_size=64,
                    epochs=10,
                    verbose=2)
scores = model.evaluate(test_x, test_y, verbose=0)

print("Accuracy: %.2f%%" % (scores[1]*100))
"""