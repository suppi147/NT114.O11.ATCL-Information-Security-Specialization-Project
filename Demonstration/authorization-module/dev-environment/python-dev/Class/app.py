from SignOperation import SignOperation
from DBinteraction import TokenManager
from AuthenPointerDBinteraction import AuthPointerManager
from DynamicTokenOperation import DynamicTokenOperation
from flask_cors import CORS 
from flask import Flask, request, make_response, render_template, jsonify
from datetime import datetime, timedelta
import jwt
from log import Logger
TIMEOUT = 2

custom_log = []

def CraftToken(userID_POST):
    logger = Logger("author_log.txt")
    signatureStage = SignOperation()
    interactDBStage = TokenManager()
    authPointerManager= AuthPointerManager()
    payload_data = {"user_id": userID_POST}
    payload_data["fingerprint"] = authPointerManager.get_fingerprint_by_uuid(userID_POST)
    payload_data["auth-service"] = authPointerManager.get_services_by_uuid(userID_POST)
    logger.log(f"|authorization-module|app.py|test_post()|crafting token with UUID:{userID_POST}, fingerprint:{authPointerManager.get_fingerprint_by_uuid(userID_POST)}, services: { authPointerManager.get_services_by_uuid(userID_POST)}|")
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
    logger = Logger("author_log.txt")
    
    if request.method == 'POST':
        authPointerManager= AuthPointerManager()
        data = request.json
        logger.log(f"|authorization-module|app.py|test_post()|recieve data :{data} from routing module|")
        username = data.get('username')
        userID_POST =authPointerManager.get_uuid_by_username(username)
        interactDBStage = TokenManager()
        logger.log(f"|authorization-module|app.py|test_post()|crafting token with UUID:{userID_POST}|")
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
    logger = Logger("author_log.txt")
    tokenRenew = DynamicTokenOperation()
    if request.method == 'POST':
        data = request.json
        token = data.get('token')
        logger.log(f"|authorization-module|app.py|getusername()|successfully recieve token:{token}|")
        action = tokenRenew.CheckValidTokenForUsername(token)
        logger.log(f"|authorization-module|app.py|getusername()|check valid token by username: {action}|")
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
            logger.log(f"|authorization-module|app.py|getusername()|extract username: {username} from uuid:{user_id} from removed tag decoded token:{payload_data}|")
            data={"username":username}
            return jsonify(data), 200
        else:
            return "something wrong",400





@app.route('/log', methods=['GET'])
def view_log():
    return custom_log,200

if __name__ == '__main__':
    app.run(debug=True)
