from flask import Flask, request, make_response, render_template, redirect,jsonify
from DBInteraction import AuthManager
from log import Logger
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
        logger = Logger("authen_log.txt")
        logger.log(f"|authentication-module|app.py|register()|getting from https://token.noteziee.cloud/register username:{username}, password:{password}, services:{services}|")
        random_uuid = uuid.uuid4()
        totpkey= pyotp.random_base32()
        encryptTotpkey= aes.encrypt_aes_cbc(totpkey)
        password = hash_function.sha3_256(password)
        logger.log(f"|authentication-module|app.py|register()|username:{username}, password:{password}, services:{services}, random_uuid:{random_uuid}, totpkey:{totpkey}, encryptTotpkey:{encryptTotpkey}, hPassword:{password}")

        
        if not username or not password or not services:
            logger.log("|authentication-module|app.py|register()|Username, password, and services are required|")
            return jsonify({"message": "Username, password, and services are required"}), 400
        elif interactDBStage.username_exists(username):
            logger.log(f"|authentication-module|app.py|register()|Username:{username} exist|")
            return jsonify({"message": "Username exist"}), 400
        else:
            serviceSum = ""
            for service in services:
                serviceSum=serviceSum+service+"_"
            interactDBStage.insert_user(random_uuid,username,password,encryptTotpkey,serviceSum)
            logger.log(f"|authentication-module|app.py|register()|Successfully created new user and service. Please save your secret key in Google Authenticator|")
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
        logger = Logger("authen_log.txt")
        logger.log(f"|authentication-module|app.py|login()|information enter: username:{username}, hpass:{password}, code:{code}, fingerprint:{fingerprint}|")

        if interactDBStage.check_login(username,password):
            returncode = totp.totp(username)
            logger.log(f"|authentication-module|app.py|login()|topt calculated:{returncode}|")
            if returncode is not None and returncode == code:
                logger.log(f"|authentication-module|app.py|login()|topt identical|")
                interactDBStage.update_fingerprint_by_username(username,fingerprint)
                data = {
                "username": username
                }
                return jsonify(data), 200
            else:
                logger.log(f"|authentication-module|app.py|login()|topt NOT identical|")
                print("the topt code is wrong",returncode,code)
                return {"error": "the topt code is wrong"}, 400
        else:
            logger.log(f"|authentication-module|app.py|login()|username:{username} and password:{password} is not correct|")
            return {"error": "username and password is not correct"}, 400

if __name__ == '__main__':
    app.run(debug=True)
