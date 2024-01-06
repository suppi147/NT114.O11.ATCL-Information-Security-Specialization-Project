from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
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
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123' 
app.config['MYSQL_DB'] = 'myDB'
SECRET_KEY = 'toan'

# Initialize MySQL
mysql = MySQL(app)

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():

    try:
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
                    "data": {"secret_key": aes.decrypt_aes_cbc(user['key'], secret_key)}
                }, 201


        elif request.method == 'POST':
            return("Please fill out the form!", "danger")
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500
    return render_template('auth/register.html')


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
                            algorithm="HS256")
                            # ).decode('utf-8')
                        response_data = {
                            "message": "Successfully fetched auth token",
                            "data": "Success Login",
                        }

                        response = make_response(jsonify(response_data))
                        response.set_cookie('token', user['token'])
                        return response            
                                
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
def get_current_user(data):
    id = data['user_id']
    current_user = model.get_by_id(id)
    return render_template('auth/user.html', username=current_user['username'], email=current_user['email'], user_id=current_user['id'])

def check_author(name_system_service, array_service):
    if name_system_service in array_service:
        return True
    return False

@app.route("/service_1", methods =["GET"])
@token_required
def get_service(current_user):
    user_service = current_user['services']
    if check_author('service_1', user_service):
        return 'Welcome to Service 1'
    return 'you are not allow to use service 1'

@app.route("/service_2", methods =["GET"])
@token_required
def get_service2(current_user):
    user_service = current_user['services']
    if check_author('service_2', user_service):
        return 'Welcome to Service 2'
    return 'you are not allow to use service 2'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=True)