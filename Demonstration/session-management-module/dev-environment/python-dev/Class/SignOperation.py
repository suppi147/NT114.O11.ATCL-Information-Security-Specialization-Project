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
    
    def Sign(self,payload_data):
        payload_data["exp"] = datetime.utcnow() + timedelta(seconds=10)
        payload_data["auth-service"] = "trigger-service1"
        self.GetSecretFromTPM()
        if SignOperation.secret == None:
            print("!!! Sign secret has not been assigned.")
        else:
            SignOperation.token = jwt.encode(payload_data, SignOperation.secret, algorithm="HS512")
        if sys.version_info < (3, 6):
            # Import the sha3 module from the pysha3 library
            from sha3 import sha3_256 as sha3_256
        else:
            sha3_256 = hashlib.sha3_256

        # Convert the key string to bytes
        key = SignOperation.secret.encode()

        # create an HMAC-SHA3-256 hash object
        hmac_sha3_256 = hmac.new(key, SignOperation.token.encode(), digestmod=sha3_256)

        # Get the hash digest as bytes
        hash_bytes = hmac_sha3_256.digest()

        # Encode the bytes in Base64
        sha3_tag = base64.b64encode(hash_bytes).decode()
        print("HMAC-SHA3-256 Hash (Base64):", sha3_tag)
        SignOperation.token= SignOperation.token +"."+sha3_tag
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
            print("tag is valid.")
        else:
            print("tag is not valid.:")
            
    def CheckSignature(self, token):
        self.GetSecretFromTPM()
        try:
            token_parts = token.split('.')
            # Extract the base64 tag after the last dot
            last_base64_tag = token_parts[-1]
            token_without_tag = token_parts[0]+"."+token_parts[1]+"."+token_parts[2]
            SignOperation.check_hmac_sha3_256_signature(token_without_tag, SignOperation.secret.encode(), last_base64_tag)
            decoded_payload = jwt.decode(token_without_tag, SignOperation.secret, algorithms=["HS512"])
            print("Token is signed with the correct secret.")
            return decoded_payload
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return False
        except jwt.InvalidTokenError:
            print("Token is not signed with the provided secret.")
        return None