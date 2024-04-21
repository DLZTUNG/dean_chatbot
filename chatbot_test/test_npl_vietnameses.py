from pyvi import ViTokenizer, ViPosTagger, ViUtils

import nltk 

def them_chuoi_vao_list(chuoi, danh_sach):
    tu = chuoi.split()  # Tách chuỗi thành các từ
    danh_sach.extend(tu)  # Thêm từng từ vào danh sách
    # Hoặc sử dụng danh_sach += tu

    return danh_sach


a = []
string = "Xin chào"
a2 = []
a2 = them_chuoi_vao_list(ViTokenizer.tokenize(string), a2)
a.extend(a2)

a1 = nltk.word_tokenize("Xin chào")

b = ViPosTagger.postagging(ViTokenizer.tokenize(u"Trường đại học Bách Khoa Hà Nội"))

c = ViUtils.remove_accents(u"Trường đại học bách khoa hà nội")

d = ViUtils.add_accents(u'truong dai hoc bach khoa ha noi')

print("\n")
print(a)
print("\n")
print(a1)
print("\n")

