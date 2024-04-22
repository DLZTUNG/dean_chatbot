import random
import json
import pickle
import numpy as np

from pyvi import ViTokenizer, ViPosTagger, ViUtils
from keras.models import load_model

# Đọc file json
file_path = 'intents.json'

with open(file_path, 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Đọc danh sách words từ tệp words.pkl
with open('words.pkl', 'rb') as file:
    words = pickle.load(file, encoding='utf-8', errors='surrogateescape')

# Đọc danh sách classes từ tệp classes.pkl
with open('classes.pkl', 'rb') as file:
    classes = pickle.load(file, encoding='utf-8', errors='surrogateescape')

model = load_model('chatbot_model.h5')

def them_chuoi_vao_list(chuoi, danh_sach):
    tu = chuoi.split()  # Tách chuỗi thành các từ
    danh_sach.extend(tu)  # Thêm từng từ vào danh sách
    # Hoặc sử dụng danh_sach += tu

    return danh_sach

def clean_up_sentence(sentence):
    sentence_words = []
    sentence_words = them_chuoi_vao_list(ViTokenizer.tokenize(sentence), sentence_words)
    return sentence_words

def bag_of_words (sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class (sentence):
    bow = bag_of_words (sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes [r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice (i['responses'])
            break
    return result

def run_chatbot(message):
    ints = predict_class (message)
    res = get_response (ints, intents)
    return res


    