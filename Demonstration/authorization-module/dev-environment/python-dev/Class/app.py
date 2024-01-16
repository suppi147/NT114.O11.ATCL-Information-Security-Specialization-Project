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
    signToken = signatureStage.Sign(payload_data,time)
    if not interactDBStage.token_exists(signToken) and not interactDBStage.uuid_exists(userID_POST):
            interactDBStage.insert_token(signToken,userID_POST)
            return "done create"
    else:
        if interactDBStage.uuid_exists(userID_POST):
            interactDBStage.update_token(userID_POST,signToken)
            return "done update"
        else:
            print("uuid not exist")
            return "somthing wrong"

    

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
"""
def renewToken(user_id):
    tokenRenew = TokenManager()
    retrieveToken = tokenRenew.get_token_by_uuid(user_id)
    time = datetime.utcnow() + timedelta(minutes=TIMEOUT)
    action = tokenRenew.CheckValidToken(retrieveToken,time)
    return action
"""
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


@app.route('/log', methods=['GET'])
def view_log():
    return custom_log,200

if __name__ == '__main__':
    app.run(debug=True)
