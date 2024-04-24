import json

# Đường dẫn đến tệp JSON
file_path = 'vietnam.json'

# Đọc dữ liệu từ tệp JSON
def load_data():
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    return json_data

# Thêm một intent mới
def add_intent(tag, patterns, responses):
    json_data = load_data()
    new_intent = {
        'tag': tag,
        'patterns': patterns,
        'responses': responses
    }
    json_data['intents'].append(new_intent)

    # Ghi dữ liệu mới vào tệp JSON
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

# Cập nhật patterns và responses cho một intent
def update_intent(tag, new_patterns, new_responses):
    json_data = load_data()
    intents = json_data['intents']
    for intent in intents:
        if intent['tag'] == tag:
            intent['patterns'].extend(new_patterns)
            intent['responses'].extend(new_responses)
        
        add_intent(tag, new_patterns, new_responses)

    # Ghi dữ liệu đã cập nhật vào tệp JSON
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)


# Kiểm tra tag tồn tại trong danh sách intents
def check_tag(tag):
    file_path = 'vietnam.json'
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    tag_exists = False
    for intent in json_data["intents"]:
        if intent["tag"] == tag:
            tag_exists = True
            break
    return tag_exists

def remove_empty(file_path):
    # Đọc dữ liệu từ file JSON
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)

    # Duyệt qua danh sách intents
    intents = data["intents"]
    for intent in intents:
        responses = intent["responses"]
        responses = [response for response in responses if response != ""]  # Lọc và loại bỏ giá trị rỗng
        intent["responses"] = responses

    for intent in intents:
        patterns = intent["patterns"]
        patterns = [pattern for pattern in patterns if pattern != ""]  # Lọc và loại bỏ giá trị rỗng
        intent["patterns"] = patterns

    # Ghi dữ liệu đã cập nhật vào file JSON
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
# Thêm một tag
#add_intent('Hỏi thăm', [], [])

# Thêm cả tag và đoạn hội thoai mới
#add_intent('Cảm ơn', ['Thanks'], ['Rất vui vì được giúp bạn!'])

# Thêm một đoạn hội thoại vào tag sẵn có
#update_intent('Hỏi thăm', ['Khỏe không cu'], ['Bố mày khỏe re'])





