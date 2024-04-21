from chatbot import run_chatbot, predict_class

while (True):
    message = input("Mời bạn nhập câu hỏi: ")
    print(predict_class(message))
    rps = run_chatbot(message)
    print(rps)
    
