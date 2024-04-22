import random
import json
import pickle
import numpy as np
import tensorflow as tf

from pyvi import ViTokenizer, ViPosTagger, ViUtils

file_path = 'intents.json'

with open(file_path, 'r', encoding='utf-8') as file:
    intents = json.load(file)

def them_chuoi_vao_list(chuoi, danh_sach):
    tu = chuoi.split()  # Tách chuỗi thành các từ
    danh_sach.extend(tu)  # Thêm từng từ vào danh sách
    # Hoặc sử dụng danh_sach += tu
    return danh_sach

words = []
classes = []
documents = []
ignoreLetters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        wordList = []
        wordList = them_chuoi_vao_list(ViTokenizer.tokenize(pattern), wordList)
        words.extend(wordList)
        documents.append((wordList, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [word for word in words if word not in ignoreLetters]

words = sorted(set(words))
classes = sorted(set(classes))

# Lưu danh sách words vào tệp words.pkl
with open('words.pkl', 'wb') as file:
    pickle.dump(words, file, protocol=pickle.HIGHEST_PROTOCOL)

# Lưu danh sách classes vào tệp classes.pkl
with open('classes.pkl', 'wb') as file:
    pickle.dump(classes, file, protocol=pickle.HIGHEST_PROTOCOL)

training = []
outputEmpty = [0] * len(classes)

for document in documents:
    bag = []
    wordPatterns = document[0]
    wordPatterns = [x.lower() for x in wordPatterns]
    for word in words:
        bag.append(1) if word in wordPatterns else bag.append(0)

    outputRow = list(outputEmpty)
    outputRow[classes.index(document[1])] = 1
    training.append(bag + outputRow)

random.shuffle(training)
training = np.array(training)

trainX = training[:, :len(words)]
trainY = training[:, len(words):]


model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(128, input_shape=(len(trainX[0]),), activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(64, activation = 'relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(len(trainY[0]), activation='softmax'))

sgd = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(trainX), np.array(trainY), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.h5', hist)
print('Done')

















