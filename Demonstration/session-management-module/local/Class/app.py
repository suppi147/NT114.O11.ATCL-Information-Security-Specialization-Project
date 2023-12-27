from SignOperation import SignOperation
from DBinteraction import TokenManager
from DynamicTokenOperation import DynamicTokenOperation
from flask_cors import CORS 
from flask import Flask, request, make_response, render_template, redirect
from datetime import datetime, timedelta

def CraftToken(userID_POST):
    signatureStage = SignOperation()
    interactDBStage = TokenManager()
    payload_data = {"user_id": userID_POST}
    payload_data["fingerprint"] = "8db79807430561f22709adb678ddfd3a"
    time = datetime.utcnow() + timedelta(minutes=2)
    signToken = signatureStage.Sign(payload_data,time)
    if not interactDBStage.token_exists(signToken):
        if not interactDBStage.uuid_exists(userID_POST):
            interactDBStage.insert_token(signToken,userID_POST)
        else:
            print("uuid exist")
    else:
        print("token exist")

def UpdateDynamicToken(userID_POST):
    payload_data = {"user_id": userID_POST}
    payload_data["fingerprint"] = "8db79807430561f22709adb678ddfd3a"
    signatureStage = SignOperation()
    interactDBStage = TokenManager()
    time = datetime.utcnow() + timedelta(minutes=2)
    signToken = signatureStage.Sign(payload_data,time)
    
    if interactDBStage.uuid_exists(userID_POST):
        interactDBStage.update_token(userID_POST,signToken)
    else:
        print("uuid not exist")


    

app = Flask(__name__)
CORS(app)

@app.route('/token', methods=['POST'])
def test_post():
    if request.method == 'POST':
        userID_POST = request.form.get('userID')
        interactDBStage = TokenManager()
        CraftToken(userID_POST)
        UpdateDynamicToken(userID_POST)
        retrieveToken = interactDBStage.get_token_by_uuid(userID_POST)
        response = make_response('token create')
        response.set_cookie('token', value=retrieveToken)
        return response
    else:
        return 'This route only accepts POST requests.'

@app.route('/renew', methods=['GET'])
def renew():
    tokenRenew = DynamicTokenOperation() 
    cookie_header = request.headers.get('Cookie')
    response = make_response('redirect')
    if cookie_header:
        cookies = cookie_header.split('; ')
        for cookie in cookies:
            if 'token=' in cookie:
                token = cookie.split('token=')[1]
                print(f'Token: {token}')
                action = tokenRenew.CheckValidToken(token)
                if action == False:
                    response = make_response('Token is fully expired')
                    response.set_cookie('token', value='NULL', expires = 0)
                elif action != None:
                    response = make_response('Token is renew')
                    response.set_cookie('token', value=action)
            
            return response
    return "hi"
    
@app.route('/')
def index():
    return render_template('createtoken.html')

if __name__ == '__main__':
    app.run(debug=True)
