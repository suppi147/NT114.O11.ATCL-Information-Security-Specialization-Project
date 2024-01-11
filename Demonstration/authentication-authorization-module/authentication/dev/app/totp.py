from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pyotp
import time
import os
import aes

app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'authen-service-db-service'
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')

def totp(username, secret_key):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT `key` FROM users WHERE username=%s', (username,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        user_key = user['key']
        key= aes.decrypt_aes_cbc(user_key, secret_key)
        totp = pyotp.TOTP(key)
        otp = totp.now()
        return otp