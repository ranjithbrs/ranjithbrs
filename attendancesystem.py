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







@app.route('/reports')
@login_required
def reports():
    if current_user.role != 'admin':
        return "Unauthorized"
    cursor.execute("""
        SELECT s.name, 
               COUNT(CASE WHEN a.status='Present' THEN 1 END)/COUNT(*)*100 AS percentage
        FROM students s
        JOIN attendance a ON s.student_id = a.student_id
        GROUP BY s.student_id
    """)
    rows = cursor.fetchall()
    labels = [row[0] for row in rows]
    data = [row[1] for row in rows]
    return render_template('reports.html', labels=labels, data=data)






    
    records = cursor.fetchall()
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)





from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector, bcrypt

app = Flask(__name__)
app.secret_key = "secret_key_here"

login_manager = LoginManager()
login_manager.init_app(app)

db = mysql.connector.connect(
    host="localhost", user="root", password="your_password", database="attendance_system"
)
cursor = db.cursor(dictionary=True)

class User(UserMixin):
    def __init__(self, id, username, role, student_id):
        self.id = id
        self.username = username
        self.role = role
        self.student_id = student_id

@login_manager.user_loader
def load_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    u = cursor.fetchone()
    if u:
        return User(u['user_id'], u['username'], u['role'], u['student_id'])
    return None

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        u = cursor.fetchone()
        if u and bcrypt.checkpw(password, u['password'].encode('utf-8')):
            user = User(u['user_id'], u['username'], u['role'], u['student_id'])
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        return f"Welcome {current_user.username}, view your attendance here."
    elif current_user.role == 'admin':
        return "Admin dashboard: view all reports."
    else:
        return "Unauthorized"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

db = mysql.connector.connect(
    host="localhost", user="root", password="your_password", database="attendance_system"
)
cursor = db.cursor()

query = """
SELECT s.name, a.date, a.status
FROM students s
JOIN attendance a ON s.student_id = a.student_id
"""
cursor.execute(query)
rows = cursor.fetchall()

# Convert to DataFrame
df = pd.DataFrame(rows, columns=['name','date','status'])

# Calculate percentage
report = df.groupby('name')['status'].apply(lambda x: (x=='Present').sum()/len(x)*100)
print(report)

# Visualization
report.plot(kind='bar', title="Attendance Percentage per Student")
plt.ylabel("Percentage (%)")
plt.show()



