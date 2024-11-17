from flask import request, render_template
import sqlite3
import time
import psycopg2
from models import db
from flask import jsonify
from random import randint


def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/get_one_rand_user', methods=['GET'])
    def get_one_rand_user():
        with psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI']) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                result = cursor.fetchall()
                one_user= result[randint(0, len(result)-1)]
        return jsonify({"username" : one_user[1]})
    
    @app.route('/classic_sqli', methods=['GET', 'POST'])
    def classic_sqli():
        return render_template('classic_sqli.html')

    @app.route('/classic_sqli_login', methods=['GET', 'POST'])
    def classic_sqli_login():
        data=request.get_json()
        if data:
            username = data['username']
            password = data['password']
            conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
            cursor = conn.cursor()
            # celowe wprowadzanie podatności sql injection
            query = f"SELECT id FROM users WHERE username = '{username}' AND password = '{password}'"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            if result:
                return jsonify({"status": "success", "message": "Login successfully", "result": result}), 200
            else:
                return jsonify({"status": "error", "message": "Invalid username or password"}), 400
        return jsonify({"status": "error", "message": "No data provided"}), 400

    @app.route('/second_order_sqli', methods=['GET', 'POST'])
    def second_order_sqli():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            with psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI']) as conn:
                with conn.cursor() as cursor:
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
