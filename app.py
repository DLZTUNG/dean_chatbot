from flask import Flask, jsonify, redirect, render_template, request, Response, url_for, json
import subprocess
import sqlite3

from add_json import add_intent, update_intent, check_tag, remove_empty
from chat import get_response_for_web

sqldbname = 'db/course_web.db'
app = Flask(__name__, static_folder='static')


#RENDER TRANG CHỦ VÀ HIỂN THỊ KHÓA HỌC
@app.route('/', methods = ['GET'])
def Load_home_page():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    querry = 'SELECT * FROM Course'
    cursor.execute(querry)
    courses_list = cursor.fetchall()

    return render_template('home.html', courses=courses_list)

#--------------------------------------------------------------------------------------------------------------

#Phương thức Post để lấy câu hỏi khi nhập vào chatbot
@app.route('/predict', methods=['POST'])
def predict():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    text = request.get_json().get('message')
    response = get_response_for_web(text)
    if (response == 'Xin lỗi vì tôi không hiểu câu hỏi của bạn, tôi vẫn đang trong quá trình phát triển.'):
        querry = "INSERT INTO UnknowQues(ques)VALUES ('{0}')"
        cursor.execute(querry.format(text))
        conn.commit()
    message = {"answer": response}
    return jsonify(message)

#--------------------------------------------------------------------------------------------------------------

#LẤY HÌNH ẢNH TỪ DATABASE
@app.route('/get_image.py')
def get_image():
    connection = sqlite3.connect(sqldbname)
    cursor = connection.cursor()
    #Lấy request từ HTML
    course_id = request.args.get('course_id')
    # Truy vấn dữ liệu hình ảnh từ cột course_image trong bảng Course
    select_query = "SELECT course_image FROM Course WHERE course_id = ?"
    cursor.execute(select_query, (course_id,))
    result = cursor.fetchone()
    
    # Lấy dữ liệu hình ảnh từ kết quả truy vấn
    image_data = result[0]
    
    # Đóng kết nối
    cursor.close()
    connection.close()

    # Trả về dữ liệu hình ảnh như một phản hồi HTTP với kiểu nội dung là image/png
    return Response(image_data, mimetype='image/png')

@app.route('/user/<username>') 
def Load_user_page(username):
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    querry = 'SELECT * FROM Course'
    cursor.execute(querry)
    courses = cursor.fetchall()
    return render_template('user.html', user = username, courses = courses)

@app.route('/<username>')
def Load_admin_page(username):
    return render_template('admin.html', user = username)

@app.route('/signin', methods=['GET'])
def Load_sign_in_page():
    return render_template("signin.html")

@app.route('/signin', methods=['POST'])
def Signin():
    if request.method == 'POST':
        connection = sqlite3.connect(sqldbname)
        cursor = connection.cursor()

        username = request.form['name']
        password = request.form['pass']
        cursor.execute("SELECT * FROM Accounts WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        connection.close()
        if user:
            if username == 'ADMIN':
                return redirect(url_for('Load_admin_page', username = username))
            
            return redirect(url_for('Load_user_page', username = username))
            
        return redirect(url_for('Load_sign_in_page')) 
    
@app.route('/ADMIN/accounts', methods = ['GET'])
def Load_accounts_page():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    querry = 'SELECT * FROM Accounts'
    cursor.execute(querry)
    account_list = cursor.fetchall()
    return render_template('account.html', list = account_list)

@app.route('/ADMIN/accounts', methods = ['POST'])
def Add_account():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    username = request.form['name']
    password = request.form['pass']
    email = request.form['email']

    querry = "INSERT INTO Accounts(username, password, email) VALUES ('{0}', '{1}', '{2}')"
    cursor.execute(querry.format(username, password, email))
    conn.commit()

    return redirect(url_for('Load_accounts_page'))

@app.route('/ADMIN/transactions')
def Load_transactions_page():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    querry = "SELECT * FROM View_trans"
    cursor.execute(querry)
    trans_list = cursor.fetchall()

    return render_template('transaction.html', list = trans_list)

@app.route('/ADMIN/courses')
def Load_courses_page():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    querry = 'SELECT * FROM Course'
    cursor.execute(querry)
    course_list = cursor.fetchall()
    return render_template('course.html', courses = course_list)

@app.route('/ADMIN/courses', methods = ['POST'])
def Add_course():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()

    course_name = request.form['name']
    course_cate = request.form['cate']
    course_desc = request.form['desc']
    course_cost = request.form['cost']

    querry = "INSERT INTO Course(course_name, category_name, course_desc, course_cost) VALUES ('{0}', '{1}', '{2}', '{3}')"
    cursor.execute(querry.format(course_name, course_cate, course_desc, course_cost))
    conn.commit()

    return redirect(url_for('Load_courses_page'))



#--------------------------------------------------------------------------------------------------------------

@app.route('/ADMIN/chatbot', methods = ['GET'])
def Load_chatbot_page():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    querry = 'SELECT * FROM UnknowQues'
    cursor.execute(querry)
    ques_list = cursor.fetchall()
    return render_template('chatbot.html', list = ques_list)

@app.route('/ADMIN/chatbot', methods=['POST'])
def Add_data_chatbot():
    tag = request.form['tag']
    pattern = request.form['pattern']
    response = request.form['response']

    if check_tag(tag):
        update_intent(tag, [pattern], [response])
    else:
        if pattern == '' and response == '':
            add_intent(tag, [], [])
        else:
            add_intent(tag, [pattern], [response])
    
    remove_empty('vietnam.json')
    return redirect(url_for('Load_chatbot_page'))

@app.route('/ADMIN/datachatbot')
def Display_json():
    with open('vietnam.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return render_template('showdatachatbot.html', data=data)

@app.route("/reset_chatbot", methods=["POST"])
def Reset_chatbot():
    try:
        # Gọi lệnh để chạy file train.py
        subprocess.run(["python", "train.py"])
        # Gọi lệnh để chạy file chat.py
        subprocess.run(["python", "chat.py"])
        
        return jsonify({"success": True})  # Trả về phản hồi thành công
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})  # Trả về phản hồi lỗi
    

@app.route("/ADMIN/chatbot", methods=["DELETE"])
def Delete_record():
    conn = sqlite3.connect(sqldbname)
    cursor = conn.cursor()
    querry = "DELETE FROM UnknowQues"
    cursor.execute(querry)
    conn.commit()
    return "Xóa thành công"  # Phản hồi thành công cho yêu cầu AJAX

#--------------------------------------------------------------------------------------------------------------


@app.route('/signup')
def Load_sign_up_page():
    return render_template("signup.html")

@app.route('/signup', methods = ['POST'])
def Signup():
    if request.method == 'POST':
        conn = sqlite3.connect(sqldbname)
        cursor = conn.cursor()

        username = request.form['name']
        password = request.form['pass']
        email = request.form['email']

        querry = "INSERT INTO Accounts(username, password, email) VALUES ('{0}', '{1}', '{2}')"
        cursor.execute(querry.format(username, password, email))
        conn.commit()

        return redirect(url_for('Load_sign_in_page'))

@app.route('/product/<coursename>')
def Load_product_page(coursename):
    connection = sqlite3.connect(sqldbname)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Course WHERE course_name = '{0}'".format((coursename)))
    course = cursor.fetchall()

    return render_template('product.html', course_name = coursename, courses = course)

@app.route('/product/<username>/<coursename>')
def Load_product_user_page(username, coursename):
    connection = sqlite3.connect(sqldbname)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Course WHERE course_name = '{0}'".format((coursename)))
    course = cursor.fetchall()
    return render_template('product_user.html', user = username, courses = course)

@app.route('/product/<username>/<coursename>', methods=['POST'])
def Buy_course(username, coursename):
    if request.method == 'POST':
        connection = sqlite3.connect(sqldbname)
        cursor = connection.cursor()
        cursor.execute("SELECT course_id FROM Course WHERE course_name = '{0}'".format((coursename)))
        result = cursor.fetchone()
        course_id = result[0]
        connection.close()
        connection = sqlite3.connect(sqldbname)
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM Accounts WHERE username = '{0}'".format((username)))
        result = cursor.fetchone()
        user_id = result[0]

        cursor.execute("INSERT INTO PurchasedCourses(user_id, course_id, date_buy) VALUES ({0}, {1}, date('now'))".format(user_id, course_id))
        connection.commit()

        return render_template('product_user.html', user = username)

if __name__ == '__main__':
    app.run(debug=True, port=8080)