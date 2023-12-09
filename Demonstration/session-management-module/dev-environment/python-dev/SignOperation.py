import jwt
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.DEBUG)
class SignOperation():
    secret = None
    token = None
    def __init__(self):
        pass
    @staticmethod
    def GetSecretFromTPM():
        SignOperation.secret="secret"
        print("Sign secret has been retreived.")
    
    def Sign(self,payload_data):
        payload_data["exp"] = datetime.utcnow() + timedelta(seconds=10)
        payload_data["auth-service"] = "trigger-service1"
        self.GetSecretFromTPM()
        if SignOperation.secret == None:
            print("!!! Sign secret has not been assigned.")
        else:
            SignOperation.token = jwt.encode(payload_data, SignOperation.secret, algorithm="HS256")
            print("token is signed: "+SignOperation.token)
            return SignOperation.token
            
    def CheckSignature(self, token):
        self.GetSecretFromTPM()
        try:
            decoded_payload = jwt.decode(token, SignOperation.secret, algorithms=["HS256"])
            print("Token is signed with the correct secret.")
            return decoded_payload
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.InvalidTokenError:
            print("Token is not signed with the provided secret.")
        return None
        
