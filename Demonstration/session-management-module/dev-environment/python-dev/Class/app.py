from SignOperation import SignOperation
from DBinteraction import TokenManager
from AuthenPointerDBinteraction import AuthPointerManager
from DynamicTokenOperation import DynamicTokenOperation
from flask_cors import CORS 
from flask import Flask, request, make_response, render_template, jsonify
from datetime import datetime, timedelta
import jwt
from log import Logger

app = Flask(__name__)

def dynamizeToken(signToken):
    token_parts = signToken.split('.')
    token_without_tag = token_parts[0]+"."+token_parts[1]+"."
    payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
    signer = SignOperation()
    token = signer.Sign(payload_data)
    updateToken = TokenManager()
    updateToken.update_token(payload_data.get('user_id'),token)
    return token

@app.route('/check', methods=['POST'])
def check():
    logger = Logger("session_log.txt")
    tokenRenew = DynamicTokenOperation()
    getFromAuth = AuthPointerManager()
    if request.method == 'POST':
        data = request.json
        token = data.get('token')
        requestService = data.get('service')
        action = tokenRenew.CheckValidTokenForUsername(token)
        logger.log(f"|session-management-module|app.py|check()|token used:{token} and requested service{requestService} with valid check {action}|")
        if action == False:
            returnData = {"token":None,"access":False}
        else:
            token_parts = token.split('.')
            token_without_tag = token_parts[0]+"."+token_parts[1]+"."
            payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
            fingerprint = payload_data.get('fingerprint')
            uuid = payload_data.get('user_id')
            allow_service = payload_data.get('auth-service')
            logger.log(f"|session-management-module|app.py|check()|exstract fingerprint:{fingerprint}, uuid:{uuid}, allow service:{allow_service} from token:{payload_data}|")
            input_string = allow_service
            services = input_string.split('_')
            services = [service for service in services if service]
            for service in services:
                if requestService == service:
                    logger.log(f"|session-management-module|app.py|check()|service allow: {service}|")
                    token = dynamizeToken(token)
                    logger.log(f"|session-management-module|app.py|check()|return dynamic token: {token}|")
                    returnData = {"token":token,"access":True}
                    return jsonify(returnData), 200
            logger.log(f"|session-management-module|app.py|check()|No service allow|")
            returnData = {"token":token,"access":False}
        return jsonify(returnData), 200
        """
            compareFingerprint = getFromAuth.get_fingerprint_by_uuid(uuid)
            if compareFingerprint != fingerprint:
                returnData = {"token":None,"access":False}
            
            

            return jsonify(returnData), 200
        """

if __name__ == '__main__':
    app.run(debug=True)
