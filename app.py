from flask import Flask, jsonify, request
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Tải biến môi trường từ tập tin .env
load_dotenv()

# Lấy giá trị từ biến môi trường DATABASE_URL
database_url = os.getenv("DATABASE_URL")
# Kết nối đến cơ sở dữ liệu MySQL
db = mysql.connector.connect(
    host=database_url.split('@')[1].split('/')[0],
    user=database_url.split('://')[1].split(':')[0],
    password=database_url.split('://')[1].split(':')[1].split('@')[0],
    database=database_url.split('/')[-1]
)

# Định nghĩa route để hiển thị danh sách sinh viên
@app.route('/students', methods=['GET'])
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM SINHVIEN")
    students = cursor.fetchall()
    cursor.close()
    # Sử dụng jsonify để chuyển đổi dữ liệu sang JSON
    student_json = []
    for student in students:
        student_json.append({
            'MSSV': student[0],
            'Name': student[1],
            'Age': student[2],
            'Class': student[3],
            'Country': student[4],
            'Gender': student[5]
        })
    
    return jsonify(student_json)

# Định nghĩa route POST để chèn dữ liệu sinh viên vào cơ sở dữ liệu
@app.route('/students', methods=['POST'])
def insert_student():
    try:
        data = request.get_json()  # Lấy dữ liệu từ request

        # Trích xuất thông tin từ dữ liệu JSON
        name = data['Name']
        age = data['Age']
        class_ = data['Class']
        country = data['Country']
        gender = data['Gender']

        # Thực hiện INSERT dữ liệu vào cơ sở dữ liệu
        cursor = db.cursor()
        query = "INSERT INTO SINHVIEN (NAME, AGE, CLASS, COUNTRY, GENDER) VALUES (%s, %s, %s, %s, %s)"
        values = (name, age, class_, country, gender)
        
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return jsonify({'message': 'Dữ liệu đã được chèn vào cơ sở dữ liệu'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Định nghĩa route GET để tìm sinh viên theo MSSV
@app.route('/students/<int:mssv>', methods=['GET'])
def find_student(mssv):
    cursor = db.cursor()
    query = "SELECT * FROM SINHVIEN WHERE MSSV = %s"
    cursor.execute(query, (mssv,))
    student = cursor.fetchone()
    cursor.close()

    if student:
        student_info = {
            'MSSV': student[0],
            'Name': student[1],
            'Age': student[2],
            'Class': student[3],
            'Country': student[4],
            'Gender': student[5]
        }
        return jsonify(student_info)
    else:
        return jsonify({'message': 'Không tìm thấy sinh viên với MSSV đã cho'})

# Định nghĩa route DELETE để xóa sinh viên theo MSSV
@app.route('/students/<int:mssv>', methods=['DELETE'])
def delete_student(mssv):
    try:
        cursor = db.cursor()
        query = "DELETE FROM SINHVIEN WHERE MSSV = %s"
        cursor.execute(query, (mssv,))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Đã xóa sinh viên có MSSV {}'.format(mssv)})
    except Exception as e:
        return jsonify({'error': str(e)})

# Định nghĩa route PUT để cập nhật thông tin sinh viên theo MSSV
@app.route('/students/<int:mssv>', methods=['PATCH'])
def update_student(mssv):
    try:
        data = request.get_json()  # Lấy dữ liệu từ request

        # Trích xuất thông tin từ dữ liệu JSON
        name = data['Name']
        age = data['Age']
        class_ = data['Class']
        country = data['Country']
        gender = data['Gender']

        cursor = db.cursor()
        query = "UPDATE SINHVIEN SET NAME=%s, AGE=%s, CLASS=%s, COUNTRY=%s, GENDER=%s WHERE MSSV=%s"
        values = (name, age, class_, country, gender, mssv)
        
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return jsonify({'message': 'Đã cập nhật thông tin sinh viên có MSSV {}'.format(mssv)})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)