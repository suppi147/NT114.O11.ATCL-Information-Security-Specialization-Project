from SignOperation import SignOperation
from DBinteraction import TokenManager
from AuthenPointerDBinteraction import AuthPointerManager
from DynamicTokenOperation import DynamicTokenOperation
from flask_cors import CORS 
from flask import Flask, request, make_response, render_template, jsonify
from datetime import datetime, timedelta
import jwt
TIMEOUT = 2

custom_log = []

def CraftToken(userID_POST):
    signatureStage = SignOperation()
    interactDBStage = TokenManager()
    authPointerManager= AuthPointerManager()
    payload_data = {"user_id": userID_POST}
    payload_data["fingerprint"] = authPointerManager.get_fingerprint_by_uuid(userID_POST)
    payload_data["auth-service"] = authPointerManager.get_services_by_uuid(userID_POST)
    time = datetime.utcnow() + timedelta(minutes=TIMEOUT)
    signToken = signatureStage.Sign(payload_data)
    if interactDBStage.uuid_exists(userID_POST):
        interactDBStage.update_token(userID_POST,signToken)
        return "done update"
    else:
         interactDBStage.insert_token(signToken,userID_POST)
         return "done create"
    
    

app = Flask(__name__)
CORS(app)

@app.route('/token', methods=['POST'])
def test_post():
    if request.method == 'POST':
        authPointerManager= AuthPointerManager()
        data = request.json
        username = data.get('username')
        userID_POST =authPointerManager.get_uuid_by_username(username)
        interactDBStage = TokenManager()
        CraftToken(userID_POST)
        retrieveToken = interactDBStage.get_token_by_uuid(userID_POST)
        token_data = {
            "token": retrieveToken
        }
        return jsonify(token_data),200
    else:
        return 'This route only accepts POST requests.'

@app.route('/getusername', methods=['POST'])
def getusername():
    tokenRenew = DynamicTokenOperation()
    if request.method == 'POST':
        data = request.json
        token = data.get('token')
        action = tokenRenew.CheckValidTokenForUsername(token)
        
        if action == False:
            print('author:Token is fully expired')
            data = {"isExpired":True}
            return jsonify(data), 400
        elif action != None:
            token_parts = token.split('.')
            token_without_tag = token_parts[0]+"."+token_parts[1]+"."
            payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
            user_id = payload_data.get('user_id')
            authPointerManager= AuthPointerManager()
            username =authPointerManager.get_username_by_uuid(user_id)
            data={"username":username}
            return jsonify(data), 200
        else:
            return "something wrong",400

@app.route('/check', methods=['POST'])
def check():
    tokenRenew = DynamicTokenOperation()
    getFromAuth = AuthPointerManager()
    if request.method == 'POST':
        data = request.json
        token = data.get('token')
        requestService = data.get('service')
        action = tokenRenew.CheckValidTokenForUsername(token)
        if action == False:
            returnData = {"token":None,"access":False}
        else:
            token_parts = action.split('.')
            token_without_tag = token_parts[0]+"."+token_parts[1]+"."
            payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
            fingerprint = payload_data.get('fingerprint')
            uuid = payload_data.get('user_id')
            allow_service = payload_data.get('auth-service')

            compareFingerprint = getFromAuth.get_fingerprint_by_uuid(uuid)
            if compareFingerprint != fingerprint:
                returnData = {"token":None,"access":False}
            
            input_string = allow_service
            services = input_string.split('_')
            services = [service for service in services if service]
            for service in services:
                if requestService == service:
                    returnData = {"token":action,"access":True}
                    return jsonify(returnData), 200
            returnData = {"token":action,"access":False}
            return jsonify(returnData), 200



@app.route('/log', methods=['GET'])
def view_log():
    return custom_log,200

if __name__ == '__main__':
    app.run(debug=True)
