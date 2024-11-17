from flask import app, current_app, render_template, request, Blueprint, url_for, redirect
import psycopg2

second_order_bp = Blueprint('second_order', __name__)

@second_order_bp.route('/second_order_sqli', methods=['GET', 'POST'])
def second_order_sqli():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with psycopg2.connect(current_app.config['DATABASE_URL']) as conn:
            with conn.cursor() as cursor:
                # UWAGA: Wrażliwe na SQL Injection, zaleca się stosowanie zapytań z parametrami!
                query = f"SELECT * FROM second_order_users WHERE username = '{username}' AND password = '{password}'"
                cursor.execute(query)
                result = cursor.fetchall()

        return render_template('second_order_sqli.html', result=result)
    return render_template('second_order_sqli.html')

@second_order_bp.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    
    conn = psycopg2.connect(current_app.config['DATABASE_URL'])
    cursor = conn.cursor()
    cursor.execute("INSERT INTO second_order_users (username, password_hash) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()
    
    return redirect(url_for('second_order.second_order_sqli'))