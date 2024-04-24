from pyvi import ViTokenizer, ViPosTagger, ViUtils

import nltk 

def split(string):
    return string.split() 

def format(list):
    result = [item.replace("_", " ") for item in list]
    return result
    

string = "Trường đại học Bách Khoa"

a1 = nltk.word_tokenize("Trường đại học Bách Khoa")




'''b = ViPosTagger.postagging(ViTokenizer.tokenize(u"Trường đại học Bách Khoa Hà Nội"))

c = ViUtils.remove_accents("Trường đại học bách khoa hà nội")

d = ViUtils.add_accents(u'truong dai hoc bach khoa ha noi')'''


a = format(split(ViTokenizer.tokenize(string)))

print(a)
print("\n")
print(a1)
print("\n")




