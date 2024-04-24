import numpy as np

from pyvi import ViTokenizer


def split(string):
    return string.split() 

def format(list):
    result = [item.replace("_", " ") for item in list]
    return result

def tokenize(sentence):
    return format(split(ViTokenizer.tokenize(sentence)))


def lower(word):
    return word.lower()


def bag_of_words(tokenized_sentence, words):
    sentence_words = [lower(word) for word in tokenized_sentence]
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words: 
            bag[idx] = 1

    return bag
