import jwt
import sys
import hashlib
import hmac
import base64
import os
from log import Logger
from datetime import datetime, timedelta
TIME_OUT=2

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
        logger = Logger("session_log.txt")
        payload_data["exp"] = datetime.utcnow() + timedelta(minutes=TIME_OUT) 
        logger.log(f"|session-management-module|SignOperation.py|Sign()|current epoch time {datetime.utcnow()}|")
        logger.log(f"|session-management-module|SignOperation.py|Sign()|expire epoch time {datetime.utcnow() + timedelta(minutes=TIME_OUT)}|")
        self.GetSecretFromTPM()
        if SignOperation.secret == None:
            logger.log(f"|session-management-module|SignOperation.py|Sign()|SignOperation.secret canNOT get|")
        else:
            SignOperation.token = jwt.encode(payload_data, key=None,algorithm=None)
            logger.log(f"|session-management-module|SignOperation.py|Sign()|token encode with payload: {payload_data} with token:{SignOperation.token}|")
        if sys.version_info < (3, 6):
            from sha3 import sha3_256 as sha3_256
        else:
            sha3_256 = hashlib.sha3_256
        key = SignOperation.secret.encode()
        hmac_sha3_256 = hmac.new(key, SignOperation.token.encode(), digestmod=sha3_256)
        hash_bytes = hmac_sha3_256.digest()
        sha3_tag = base64.b64encode(hash_bytes).decode()
        logger.log(f"|session-management-module|SignOperation.py|Sign()|sign token with tag {sha3_tag}")
        SignOperation.token= SignOperation.token +sha3_tag
        logger.log(f"|session-management-module|SignOperation.py|Sign()|signed token {SignOperation.token}")
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
        logger = Logger("session_log.txt")        
        
        token_parts = token.split('.')
        # Extract the base64 tag after the last dot
        last_base64_tag = token_parts[2]
        token_without_tag = token_parts[0]+"."+token_parts[1]+"."
        print("token_without_tag:",token_without_tag)
        print("last_base64_tag:",last_base64_tag)
        logger.log(f"|session-management-module|SignOperation.py|CheckSignature()|last_base64_tag: {last_base64_tag}|")
        check=SignOperation.check_hmac_sha3_256_signature(token_without_tag, SignOperation.secret.encode(), last_base64_tag)
        if check == True:
            payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
            logger.log(f"|session-management-module|SignOperation.py|CheckSignature()| decoded token is signed with right signature: {payload_data}|")
            expiration_time = payload_data.get("exp")
            if expiration_time:
                expiration_datetime = datetime.utcfromtimestamp(expiration_time)
                current_datetime = datetime.utcnow()
                if current_datetime < expiration_datetime:
                    logger.log(f"|session-management-module|SignOperation.py|CheckSignature()| decoded token is NOT expired current_datetime: {current_datetime} < expiration_datetime:{expiration_datetime}|")
                    return payload_data
                else:
                    logger.log(f"|session-management-module|SignOperation.py|CheckSignature()| decoded token is expired current_datetime: {current_datetime} > expiration_datetime:{expiration_datetime}|")
                    return False
            else:
                logger.log(f"|session-management-module|SignOperation.py|CheckSignature()| Token does not contain an expiration time.")   
                return None
        else:
            logger.log(f"|session-management-module|SignOperation.py|CheckSignature()|Token is not signed with the provided secret.|")
            return None        

