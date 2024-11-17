import sqlite3
import time
from random import randint

import psycopg2
from flask import (current_app, jsonify, redirect, render_template, request,
                   url_for)
from models import db


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
                    query = f"SELECT * FROM second_order_users WHERE username = '{username}' AND password = '{password}'"
                    cursor.execute(query)
                    result = cursor.fetchall()

            return render_template('second_order_sqli.html', result=result)
        return render_template('second_order_sqli.html')
    
    @app.route('/signup', methods=['POST'])
    def signup():
        username = request.json.get('username')
        password = request.json.get('password')
        
        conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
        cursor = conn.cursor()
        cursor.execute("INSERT INTO second_order_users (username, password_hash) VALUES (%s, %s)", (username, password))
        conn.commit()
        conn.close()
        
        return redirect(url_for('second_order_sqli'))
    
    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get('username')
        password = request.json.get('password')
        
        conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
        cursor = conn.cursor()
        
        query = f"SELECT * FROM second_order_users WHERE password_hash = '{password}' AND username = '{username}'"    # solution: username' OR '''' = '''
        cursor.execute(query)
        result = cursor.fetchall()
        
        result_list = [list(row) for row in result]
        result_list1 = "\n".join([" ".join(map(str, row)) for row in result_list])
        print(result_list1)
        
        if len(result_list) > 1:
            return jsonify({"feedback": "Success Attack", "message": result_list1}), 200
        elif len(result_list) == 1:
            return jsonify({"feedback": "Failed Attack, Success Login", "message": result_list1}), 200
        else:
            return jsonify({"feedback": "Faild Attack, Faild Login", "message": "Login failed!"}), 401

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

    @app.route('/error_based_sqli', methods=['GET', 'POST'])
    def error_based_sqli():
        result = None
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            with psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI']) as conn:
                with conn.cursor() as cursor:
                    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
                    cursor.execute(query)
                    result = cursor.fetchall()
            # Przekazujemy wynik do szablonu
        return render_template('error_based_sqli.html', result=result)


    @app.route('/out_of_band_sqli', methods=['GET', 'POST'])
    def out_of_band_sqli():
        if request.method == 'POST':
            data = request.get_json()
            if data:
                username = data['username']
                password = data['password']
                conn = psycopg2.connect(app.config['SQLALCHEMY_DATABASE_URI'])
                cursor = conn.cursor()
                # Celowe wprowadzanie podatności SQL Injection
                cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
                conn.commit()
                conn.close()
                return jsonify({"status": "success", "message": "Out-of-Band SQL Injection executed"}), 200
            return jsonify({"status": "error", "message": "No data provided"}), 400
        return render_template('out_of_band_sqli.html')
