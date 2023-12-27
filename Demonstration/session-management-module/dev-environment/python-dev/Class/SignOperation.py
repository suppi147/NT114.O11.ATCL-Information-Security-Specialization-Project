import jwt
import sys
import hashlib
import hmac
import base64
import os
from datetime import datetime, timedelta


class SignOperation():
    secret = None
    token = None
    def __init__(self):
        pass
    @staticmethod
    def GetSecretFromTPM():
        hexSecret=os.environ.get('SIGN_KEY')
        byte_data = bytes.fromhex(hexSecret)
        SignOperation.secret = base64.b64encode(byte_data).decode('utf-8')
        print("Sign secret has been retreived.")
    
    
    def Sign(self,payload_data,time):
        payload_data["exp"] = time
        self.GetSecretFromTPM()
        if SignOperation.secret == None:
            print("!!! Sign secret has not been assigned.")
        else:
            SignOperation.token = jwt.encode(payload_data, key=None,algorithm=None)
        if sys.version_info < (3, 6):
            from sha3 import sha3_256 as sha3_256
        else:
            sha3_256 = hashlib.sha3_256
        key = SignOperation.secret.encode()
        hmac_sha3_256 = hmac.new(key, SignOperation.token.encode(), digestmod=sha3_256)
        hash_bytes = hmac_sha3_256.digest()
        sha3_tag = base64.b64encode(hash_bytes).decode()
        print("HMAC-SHA3-256 Hash (Base64):", sha3_tag)
        SignOperation.token= SignOperation.token +sha3_tag
        print("token is signed: "+SignOperation.token)
        return SignOperation.token
    
    @staticmethod
    def calculate_hmac_sha3_256(data, key):
        hmac_sha3_256 = hmac.new(key, data.encode(), digestmod=hashlib.sha3_256)
        return hmac_sha3_256.digest()
    @staticmethod
    def check_hmac_sha3_256_signature(data, key, expected_signature):
        
        calculated_signature = SignOperation.calculate_hmac_sha3_256(data, key)

        if calculated_signature == base64.b64decode(expected_signature):
            return True
        else:
            return False
            
    def CheckSignature(self, token):
        self.GetSecretFromTPM()
        
        token_parts = token.split('.')
        # Extract the base64 tag after the last dot
        last_base64_tag = token_parts[2]
        token_without_tag = token_parts[0]+"."+token_parts[1]+"."
        print("token_without_tag:",token_without_tag)
        print("last_base64_tag:",last_base64_tag)

        check=SignOperation.check_hmac_sha3_256_signature(token_without_tag, SignOperation.secret.encode(), last_base64_tag)
        if check == True:
            payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
            print("Token is signed with the correct secret.")
            expiration_time = payload_data.get("exp")
            if expiration_time:
                expiration_datetime = datetime.utcfromtimestamp(expiration_time)
                current_datetime = datetime.utcnow()
                if current_datetime < expiration_datetime:
                    print("Token is not expired.")
                    return payload_data
                else:
                    print("Token has expired.")
                    return False
            else:
                print("Token does not contain an expiration time.")   
                return None
        else:
            print("Token is not signed with the provided secret.")
            return None        

