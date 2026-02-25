from flask import Flask, render_template, request, redirect, session
from db_config import get_connection

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']
            return redirect('/admin' if user['role'] == 'admin' else '/employee')
        else:
            return "Login failed"
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('role') != 'admin':
        return redirect('/')
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO tasks (title, description, assigned_to, deadline) VALUES (%s, %s, %s, %s)",
            (request.form['title'], request.form['description'], request.form['assigned_to'], request.form['deadline'])
        )
        conn.commit()

    cursor.execute("SELECT * FROM users WHERE role='employee'")
    employees = cursor.fetchall()

    return render_template('admin.html', employees=employees)

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if session.get('role') != 'employee':
        return redirect('/')
    
    user_id = session['user_id']
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO time_logs (user_id, task_id, date, hours) VALUES (%s, %s, %s, %s)",
            (user_id, request.form['task_id'], request.form['date'], request.form['hours'])
        )
        conn.commit()

    cursor.execute("SELECT * FROM tasks WHERE assigned_to=%s", (user_id,))
    tasks = cursor.fetchall()

    cursor.execute("SELECT t.title, l.date, l.hours FROM time_logs l JOIN tasks t ON l.task_id = t.id WHERE l.user_id=%s", (user_id,))
    logs = cursor.fetchall()

    return render_template('employee.html', tasks=tasks, logs=logs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
