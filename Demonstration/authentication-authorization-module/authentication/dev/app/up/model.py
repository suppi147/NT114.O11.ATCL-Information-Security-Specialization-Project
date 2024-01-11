from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'authen-service-db-service'
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')

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


       