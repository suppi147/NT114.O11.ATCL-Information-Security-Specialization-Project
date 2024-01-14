from SignOperation import SignOperation
from DBinteraction import TokenManager
from AuthenPointerDBinteraction import AuthPointerManager
from DynamicTokenOperation import DynamicTokenOperation
from flask_cors import CORS 
from flask import Flask, request, make_response, render_template, jsonify
from datetime import datetime, timedelta

TIMEOUT = 2

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

@app.route('/renew', methods=['GET'])
def renew():
    tokenRenew = DynamicTokenOperation() 
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                print(f'Token: {token}')
                time = datetime.utcnow() + timedelta(minutes=TIMEOUT)
                action = tokenRenew.CheckValidToken(token,time)
                response = None
                if action == False:
                    response = make_response('Token is fully expired')
                    response.set_cookie('token', value='NULL', expires = 0)
                elif action != None:
                    response = make_response('Token is renew')
                    response.set_cookie('token', value=action)
                else:
                    return "something wrong"
            return response
    return "hi"
    
@app.route('/create')
def index():
    return render_template('createtoken.html')

if __name__ == '__main__':
    app.run(debug=True)
