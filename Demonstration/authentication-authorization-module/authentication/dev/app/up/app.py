from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_mysqldb import MySQL
import model
import os
app = Flask(__name__)

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'authen-service-db-service'
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')


@app.route("/user/", methods=["GET"])
def get_current_user():
    id = 1
    current_user = model.get_by_id(id)
    if current_user == None:
        print("user cannot be retrieve by id")
    else:
        return render_template('auth/user.html', username=current_user['username'], email=current_user['email'], user_id=current_user['id'])


if __name__ == '__main__':
    app.run(debug=True)