from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import aes
import hash_function
import pyotp

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123' 
app.config['MYSQL_DB'] = 'myDB'

secret_key = 'asdfghjklqwertyu'


    # """User Model"""
def create(**arg):
        username = arg.get('username')
        password = arg.get('password')
        email = arg.get('email')
        key = pyotp.random_base32()
        key2 = aes.encrypt_aes_cbc(key,secret_key)
        user = get_user(username)
        if user:
            return False
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        password2 = hash_function.sha3_256(password)
        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s)', (username, password2, email, key2))
        mysql.connection.commit()
        return get_user(username)

def get_user(username):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE username LIKE %s", [username])
        user = cursor.fetchone()
        if user:
            return user

def get_by_id(id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE id = %s", [id])
        user = cursor.fetchone()
        if user:
            return user
def login(username, password):
        # """Login a user"""
        password2= hash_function.sha3_256(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password2))
        account = cursor.fetchone()
        return account

def create_fingerprint(username, fingerprint):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO fingerprint VALUES (NULL, %s, %s)', (username, fingerprint))
        mysql.connection.commit()
        return True

def register_service(userid, service):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO services VALUES (%s, %s)', (userid, service))
        mysql.connection.commit()
        return True

def get_key_user(username):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT `key` FROM users WHERE username=%s', (username,))
        user = cursor.fetchone()  # Sử dụng fetchone() thay vì fetchall() để chỉ lấy một dòng dữ liệu
        cursor.close()
        user_key = user['key']
        key= aes.decrypt_aes_cbc(user_key, secret_key)
        return key

def get_id_user(username):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone() 
        if user_id:
                return user_id["id"]
        return False

def get_service(user_id):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM services WHERE user_id = %s', (user_id,))
        service = cursor.fetchall()
        if service:
                service_names = [service['service_name'] for service in service]
                result_string = ', '.join(service_names)
                return result_string
        return False