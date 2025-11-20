from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# DB connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="attendance_system"
)
cursor = db.cursor(dictionary=True)

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data['student_id']
    date = data['date']
    status = data['status']
    query = "INSERT INTO attendance (student_id, date, status) VALUES (%s, %s, %s)"
    cursor.execute(query, (student_id, date, status))
    db.commit()
    return jsonify({"message": "Attendance marked successfully!"})

@app.route('/view_attendance/<int:student_id>', methods=['GET'])
def view_attendance(student_id):
    query = "SELECT date, status FROM attendance WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    records = cursor.fetchall()
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)
