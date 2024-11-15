from urllib.parse import quote_plus
from flask import Flask, request, render_template
import sqlite3
import time
import psycopg2
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="../frontend/templates", static_folder='../frontend/static')
CORS(app)

# postgresql://postgres:AGpiPAbmsPgaHZpsluaMjHvvXRigJVjr@autorack.proxy.rlwy.net:13722/railway

password = quote_plus(os.getenv('DB_PASSWORD', 'AGpiPAbmsPgaHZpsluaMjHvvXRigJVjr'))
db_host = os.getenv('DB_HOST', 'autorack.proxy.rlwy.net')
db_port = os.getenv('DB_PORT', '13722')
db_name = os.getenv('DB_NAME', 'railway')
db_user = os.getenv('DB_USER', 'postgres')

DATABASE_URL = f"postgresql://{db_user}:{password}@{db_host}:{db_port}/{db_name}"



#sql alchemy lets map database into the code
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AGpiPAbmsPgaHZpsluaMjHvvXRigJVjr@autorack.proxy.rlwy.net:13722/railway'  #setting up the localization of database
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class Entry(db.Model):  #table's name is created based on class name, but converted to lower case
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(20), nullable=False)
    entry_type = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

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

@app.route('/second_order_sqli', methods=['GET', 'POST'])
def second_order_sqli():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:
                # UWAGA: Wrażliwe na SQL Injection, zaleca się stosowanie zapytań z parametrami!
                query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                cursor.execute(query)
                result = cursor.fetchall()

        return render_template('second_order_sqli.html', result=result)
    return render_template('second_order_sqli.html')

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

port = int(os.environ.get('PORT', 5112))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=port, debug=True)