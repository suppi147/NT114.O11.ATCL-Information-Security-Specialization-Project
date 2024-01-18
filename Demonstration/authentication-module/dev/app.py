from flask import Flask, request, make_response, render_template, redirect,jsonify
from DBInteraction import AuthManager
import uuid
import pyotp
import aes
import hash_function
import totp

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        interactDBStage = AuthManager()
        username = data.get('username')
        password = data.get('password')
        services = data.get("services")

        random_uuid = uuid.uuid4()
        totpkey= pyotp.random_base32()
        encryptTotpkey= aes.encrypt_aes_cbc(totpkey)
        password = hash_function.sha3_256(password)
        
        if not username or not password or not services:
            return jsonify({"message": "Username, password, and services are required"}), 400
        elif interactDBStage.username_exists(username):
            return jsonify({"message": "Username exist"}), 400
        else:
            serviceSum = ""
            for service in services:
                serviceSum=serviceSum+service+"_"
            interactDBStage.insert_user(random_uuid,username,password,encryptTotpkey,serviceSum)
            return {
                    "message": "Successfully created new user and service. Please save your secret key in Google Authenticator",
                    "secret_key": totpkey
                    }, 201
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.json
        interactDBStage = AuthManager()
        username = data.get('username')
        password = data.get('password')
        password = hash_function.sha3_256(password)
        code = data.get('otp')
        fingerprint = data.get('fingerprint')

        if interactDBStage.check_login(username,password):
            returncode = totp.totp(username)
            if returncode is not None and returncode == code:      
                interactDBStage.update_fingerprint_by_username(username,fingerprint)
                data = {
                "username": username
                }
                return jsonify(data), 200
            else:
                print("the topt code is wrong",returncode,code)
                return {"error": "the topt code is wrong"}, 400
        else:
            print("something wrong with checkin")
            return {"error": "Something went wrong"}, 400

if __name__ == '__main__':
    app.run(debug=True)
