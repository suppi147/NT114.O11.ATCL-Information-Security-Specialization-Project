from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pyotp
import time
import aes

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123' 
app.config['MYSQL_DB'] = 'myDB'

def totp(username, secret_key):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT `key` FROM users WHERE username=%s', (username,))
    user = cursor.fetchone()  # Sử dụng fetchone() thay vì fetchall() để chỉ lấy một dòng dữ liệu
    cursor.close()

    if user:
        user_key = user['key']
        key= aes.decrypt_aes_cbc(user_key, secret_key)
        totp = pyotp.TOTP(key)
        otp = totp.now()
        return otp