import random
import json
import pickle
import numpy as np
import tensorflow as tf

import nltk
from pyvi import ViTokenizer, ViPosTagger, ViUtils
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('vietnameses.json', encoding='utf-8').read())

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

print("\n")
print(words)
print("\n")
print(classes)
print("\n")










