from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import totp
import validate 
import model
import jwt
import aes
from auth_middleware import token_required
app = Flask(__name__)

secret_key = 'asdfghjklqwertyu'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123' 
app.config['MYSQL_DB'] = 'myDB'
SECRET_KEY = 'toan'

# Initialize MySQL
mysql = MySQL(app)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        data = request.json
        services = data.get("services")

        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate.validate_user(**data)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        
        user = model.create(**data)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        else: 
            for service in services:
                model.register_service(user['id'],service)
            return {
            "message": "Successfully created new user and service. Please save your secret key in Google Authenticator",
            "secret key": aes.decrypt_aes_cbc(user['key'], secret_key)
            }, 201

    elif request.method == 'POST':
        return("Please fill out the form!", "danger")

@app.route("/services/", methods=["GET", "POST"])
def service_1():
    if request.method == "GET":
        # username = 'conmeo'
        username = model.get_by_id('8')
        id = model.get_user(username['username'])
        service = model.get_service(id)
        return id
    elif request.method == "POST":
        data = request.json
        services = data.get("services")
        for service in services:
            model.register_service('2',service)
        return jsonify(services)

# Login route
@app.route('/login/', methods=['GET','POST'])
def login():
    
    try:
        if request.method == 'POST':
            data = request.json
            otp = request.json["otp"]
            if not data:
                return {
                    "message": "Please provide user details",
                    "data": None,
                    "error": "Bad request"
                }, 400

            is_validated = validate.validate_email_and_password(data.get('username'), data.get('password'))
            if is_validated is not True:
                return dict(message='Invalid data', data= None, error=is_validated), 400
            user = model.login(
                data["username"],
                data["password"],
                )
            
            if user:
                if otp == totp.totp(user['username'],secret_key):
                    try:
                        id = model.get_id_user(data["username"])
                        service = model.get_service(id)
                    # token should expire after 24 hrs
                        fingerprint = data['fingerprint']
                        user["token"] = jwt.encode(
                            {"user_id": id, "services" : service, "fingerprint": fingerprint},
                            SECRET_KEY,
                            algorithm="HS256"
                            ).decode('utf-8')
                        return {
                            "message": "Successfully fetched auth token",
                            "data": user['token']
                            }
                    except Exception as e:
                        return {
                            "error": "Something went wrong2",
                            "message": str(e)
                            }, 500
                else: 
                    return {
                        "error": 'Wrong OTP',
                        "data": None
                        }, 500
                
            return {
                "message": "Error fetching auth token!, invalid email or password",
                "data": None,
                "error": "Unauthorized"
            }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500
    return render_template('auth/login.html')

@app.route("/user/", methods=["GET"])
@token_required
def get_current_user(current_user):
    # service = 'service_1'
    return jsonify({
        "username": current_user['username'],
        "email": current_user['email'],
        "user id": current_user['id']
    })    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=True)