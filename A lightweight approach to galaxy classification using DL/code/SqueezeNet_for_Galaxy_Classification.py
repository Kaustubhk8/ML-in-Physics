#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install astroNN')


# In[ ]:


from astroNN.datasets import galaxy10
from astroNN.datasets.galaxy10 import galaxy10cls_lookup
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, GlobalAveragePooling2D, Concatenate, Input, GlobalMaxPooling2D
from keras.layers import Conv2D, MaxPooling2D, ReLU, AveragePooling2D, Activation, BatchNormalization, DepthwiseConv2D, SeparableConv2D
from keras.utils import to_categorical
from keras.preprocessing import image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from keras import Model
from keras import backend as K


# In[ ]:


from tensorflow.keras.utils import image_dataset_from_directory
import tensorflow as tf
import matplotlib.pyplot as plt


# In[ ]:


import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# In[ ]:


#df = galaxy10.load_data('/content')
images, labels = galaxy10.load_data()
labels = labels.astype(np.float32)
#labels = labels.astype(int)
labels = to_categorical(labels)
images = images.astype(np.float32)
images = images/255


# In[ ]:


def show_image(image_data,label):
    label = galaxy10cls_lookup(int(label))
    plt.imshow(image_data)
    plt.title(label)
    plt.show()
for i in range(8):
    show_image(images[i], i)


# In[ ]:


def class_distribution(x, y, labels):
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_xticklabels(labels, rotation=90)
    plt.show()
    
class_distribution(features, counts, features)


# In[ ]:


X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size = 0.15)
print(X_train.shape)
print(y_train.shape)


# In[ ]:


print(X_test.shape)


# In[ ]:


def SqueezeNet(input_shape, n_classes): 
  def fire(m, fs, fe):
    s = Conv2D(fs, 1, activation='relu')(m)
    e1 = Conv2D(fe, 1, activation='relu')(s)
    e3 = Conv2D(fe, 3, padding='same', activation='relu')(s)
    output = Concatenate()([e1, e3])
    return output


  input = Input(input_shape)  

  m = Conv2D(96, 7, strides=2, padding='same', activation='relu')(input)
  m = MaxPooling2D(3, strides=2, padding='same')(m)

  m = fire(m, 16, 64)
  m = fire(m, 16, 64)
  m = fire(m, 32, 128)
  m = MaxPooling2D(3, strides=2, padding='same')(m)
  

  m = fire(m, 32, 128)
  m = fire(m, 48, 192)
  m = fire(m, 48, 192)
  m = fire(m, 64, 256)
  m = MaxPooling2D(3, strides=2, padding='same')(m)
  #m = Flatten(input_shape=(IMG_SHAPE[0], IMG_SHAPE[1], 3))(m).  #improper shape
  #m = Dense(config.hidden_nodes, activation = 'relu')(m)


  m = fire(m, 64, 256)
  m = Conv2D(n_classes, 1)(m)
  m = GlobalAveragePooling2D()(m) #Add dense layer and activation will be softmax
  #m = Flatten()(m)
  #m = Dense(10, activation = 'softmax')(m)


  output = Activation('softmax')(m)


  model = Model(input, output)
  return model


# In[ ]:


input_shape = (69, 69, 3)
n_classes = 10
K.clear_session()
model = SqueezeNet(input_shape, n_classes)
model.summary()


# In[ ]:


model.compile(optimizer='adamax', loss='categorical_crossentropy', metrics=['accuracy'])


# In[ ]:


epochs = 50
history = model.fit
model.fit(X_train, y_train, epochs = epochs, validation_data = (X_test, y_test))


# In[ ]:


epochs = 100
history = model.fit
model.fit(X_train, y_train, epochs = epochs, validation_data = (X_test, y_test))


# In[ ]:


y_pred = model.predict(X_test)


# In[ ]:


y_pred=np.argmax(y_pred, axis=1)
y_test=np.argmax(y_test, axis=1)


# In[ ]:


from sklearn.metrics import confusion_matrix


# In[ ]:


from sklearn.metrics import classification_report


# In[ ]:


class_rep = classification_report(y_test, y_pred)


# In[ ]:


X_train.shape


# In[ ]:


print(class_rep)


# In[ ]:


cm = confusion_matrix(y_test, y_pred)
print(cm)



# Overall Accuracy 
# 
# = (Sum of True Positives)/(Sum of entire matrix)
# 
# = 0.8
# 
# = 80%

# In[ ]:


epochs = 50
history = model.fit
model.fit(X_train, y_train, epochs = epochs, validation_data = (X_test, y_test))


# In[ ]:


plt.plot(model.history.history['loss'],color='b',
label='Training Loss')
plt.plot(model.history.history['val_loss'],color='r',
label='Validation Loss')
plt.legend()
plt.show()


# In[ ]:


plt.plot(model.history.history['accuracy'],color='b',
label='Training  Accuracy')
plt.plot(model.history.history['val_accuracy'],color='r',
label='Validation Accuracy')
plt.legend()
plt.show()
