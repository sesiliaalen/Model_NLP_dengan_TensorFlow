# -*- coding: utf-8 -*-
"""modul7-nlp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fTP26f0uZYsqee1oapsVPHVTpMsxd7dI

**Data Diri**

*   Nama  :Cecilia Charlene Siani Silvyana Halim
*   Email : sesiliaalen12@gmail.com
"""

from google.colab import files
uploaded = files.upload()

import pandas as pd
df = pd.read_csv('tweets.csv')
df = df.drop(columns=['id','keyword','location'])
df.head()

import tensorflow as tf

token = tf.keras.preprocessing.text.Tokenizer(num_words=3000)
token.fit_on_texts(df['text'])
x_encoded = token.texts_to_sequences(df['text'])
x = tf.keras.preprocessing.sequence.pad_sequences(x_encoded, maxlen=300)
y = df['target']
print("X: {}\nY: {}".format(len(x), len(y)))

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(3000, 100, input_length=x.shape[1]))
model.add(tf.keras.layers.LSTM(64))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.summary()

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.95):
      print("\nAkurasi telah mencapai >95%!")
      self.model.stop_training = True
callbacks = myCallback()

hist = model.fit(x, y, epochs=20, validation_data=(x_test, y_test), callbacks=[callbacks])

import matplotlib.pyplot as plt
import seaborn as sns

plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Akurasi Model')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc = 'upper left')
plt.show()

plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Loss Model')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc = 'upper left')
plt.show()

