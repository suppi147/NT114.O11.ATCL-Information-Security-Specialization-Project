from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import aes
import hash_function
import os
import pyotp

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'authen-service-db-service'
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')

secret_key = os.environ.get('authen-totp-secret-key')

def create(**arg):
    username = arg.get('username')
    password = arg.get('password')
    email = arg.get('email')
    key = pyotp.random_base32()
    key2 = aes.encrypt_aes_cbc(key,secret_key)
    user = get_user(username)
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            password2 = hash_function.sha3_256(password)
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s)', (username, password2, email, key2))
            mysql.connection.commit()
            return get_user(username)
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None

def get_user(username):
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE username LIKE %s", [username])
            user = cursor.fetchone()
            if user:
                return user
            else:
                break
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None


def get_by_id(id):
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE id = %s", [id])
            user = cursor.fetchone()
            if user:
                return user
            else:
                break
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None

def login(username, password):
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            password2= hash_function.sha3_256(password)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password2))
            user = cursor.fetchone()
            if user:
                return user
            else:
                break
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None

def get_key_user(username):
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT `key` FROM users WHERE username=%s', (username,))
            user = cursor.fetchone()
            user_key = user['key']
            key= aes.decrypt_aes_cbc(user_key, secret_key)
            if key:
                return key
            else:
                break
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None

def get_id_user(username):
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
            user_id = cursor.fetchone()
            if user_id:
                return user_id["id"]
            else:
                break
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None


def get_service(user_id):
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM services WHERE user_id = %s', (user_id,))
            service = cursor.fetchall()
            if service:
                service_names = [service['service_name'] for service in service]
                result_string = ', '.join(service_names)
                return result_string
            return False
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None

def register_service(userid, service):
    max_attempts = 1000
    attempts = 0
    while attempts < max_attempts:
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO services VALUES (%s, %s)', (userid, service))
            mysql.connection.commit()
            break
        except MySQLdb.Error as e:
            print(f"Error accessing the database: {e}")
            attempts += 1
    return None


       

