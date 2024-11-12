from flask import Flask, request, render_template
import sqlite3
import time

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    cursor.execute('''INSERT INTO users (username, password) VALUES ('admin', 'admin')''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classic_sqli', methods=['GET', 'POST'])
def classic_sqli():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return render_template('classic_sqli.html', result=result)
    return render_template('classic_sqli.html')

@app.route('/blind_sqli', methods=['GET', 'POST'])
def blind_sqli():
    if request.method == 'POST':
        username = request.form['username']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return render_template('blind_sqli.html', result=result)
    return render_template('blind_sqli.html')

@app.route('/time_based_sqli', methods=['GET', 'POST'])
def time_based_sqli():
    if request.method == 'POST':
        username = request.form['username']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}'"
        start_time = time.time()
        cursor.execute(query)
        result = cursor.fetchall()
        end_time = time.time()
        conn.close()
        return render_template('time_based_sqli.html', result=result, time_taken=end_time - start_time)
    return render_template('time_based_sqli.html')

# Add routes for other SQL Injection types similarly...

if __name__ == '__main__':
    init_db()
    app.run(debug=True)