import tensorflow as tf
import cv2
import os
import numpy as np
import ssl

# remove validation for ssl
ssl._create_default_https_context = ssl._create_unverified_context
path = '/Users/edz/Documents/recog'


# s = [0,2,3,4,6]
# x = [1]
# fashion_mnist = tf.keras.datasets.fashion_mnist
# (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
# Train = []
# Labels = []
# for i in range(train_labels.shape[0]):
#     if train_labels[i] in x:
#         Train.append(train_images[i])
#         Labels.append(0)
#     if train_labels[i] in s:
#         Train.append(train_images[i])
#         Labels.append(1)
# train_images = np.array(Train)
# train_labels = np.array(Labels)





def resize(img):
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    width = 28
    height = 28
    dim = (width, height)
    # resize image
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # cv2.imwrite('wocao2.png', img)
    return img

data_set = []
tag_set = []
for img in sorted(os.listdir(path)):
    data_set.append(resize(path + "/" + img))
train_images = data_set[:100]
test_images = data_set
train_images = np.array(train_images)
test_images = np.array(test_images)
# print(sorted(os.listdir(path)))
tag_set = [1,1,1,1,1,1,0,0,0,1,
           1,1,1,1,0,0,1,1,1,1,
           1,1,1,0,1,1,1,1,1,1,
           0,0,0,0,1,1,1,1,1,1,
           1,1,1,1,1,1,0,1,1,1,
           1,0,0,1,1,1,1,1,1,1,
           0,0,0,0,0,0,1,1,1,1,
           1,1,1,1,1,1,1,0,1,1,
           0,0,0,0,0,1,1,1,1,0,
           0,1,1,1,1,1,1,1,1,1,
           1,1,1,1,1,1,1,1,1,0,
           0,0,1,1,0,1,1,1,1,1,
           1,0,0,0,1,1,1,1,1,1,
           0]
train_labels = np.array(tag_set[:100])
test_labels = np.array(tag_set)

train_images = train_images / 255.0
test_images = test_images / 255.0
train_images=train_images.reshape(train_images.shape[0],28,28,1)
test_images=test_images.reshape(test_images.shape[0],28,28,1)
# model = tf.keras.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(1000, activation='relu'),
#     tf.keras.layers.Dense(2)
# ])
model=tf.keras.Sequential()

model.add(tf.keras.layers.Conv2D(filters=32,
                 kernel_size=(3,3),
                 padding='same',
                 input_shape=(28,28,1),
                 activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Conv2D(filters=64,
                 kernel_size=(3,3),
                 padding='same',
                 activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Conv2D(filters=128,
                 kernel_size=(3,3),
                 padding='same',
                 activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Conv2D(filters=256,
                 kernel_size=(3,3),
                 padding='same',
                 activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2,2)))
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Dense(1024,activation='relu'))
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Dense(2,activation='softmax'))

model.compile(optimizer='adam',
              loss=tf.keras.losses.sparse_categorical_crossentropy,
              metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=5)
probability_model = tf.keras.Sequential([model,  tf.keras.layers.Softmax()])
print(test_images.shape)
print(test_labels)
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

# pre_img = resize('resized.png')
# pre_img=pre_img.reshape(28,28,1)
# predictions_single = probability_model.predict(pre_img)
# print(np.argmax(predictions_single[0]))


