from SignOperation import SignOperation
from DBinteraction import TokenManager
from datetime import datetime, timedelta


class DynamicTokenOperation():
    secret = None
    token = None
    def __init__(self):
        pass
    @staticmethod
    def GetSecretFromTPM():
        DynamicTokenOperation.secret="secret"
        print("Sign secret has been retreived.")
    @staticmethod
    def UpdateNullToken(userID_POST):
        token = None
        interactDBStage = TokenManager()
        if interactDBStage.uuid_exists(userID_POST):
            interactDBStage.update_token(userID_POST,token)
        else:
            print("uuid not exist")
    @staticmethod        
    def UpdateDynamicToken(uuid,token):
        interactDBStage = TokenManager()
        interactDBStage.update_token(uuid,token)
        

    def CheckValidToken(self,signToken):
        interactDBStage = TokenManager()
        signatureStage = SignOperation()

        if interactDBStage.token_exists(signToken):
            print("token exist in DB")
            payload = signatureStage.CheckSignature(signToken)
            uuid=interactDBStage.get_uuid_by_token(signToken)
            if payload == False:
                print("token fully expired")
                
                DynamicTokenOperation.UpdateNullToken(uuid)
                return False
            if payload != None:
                time = datetime.utcnow() + timedelta(minutes=5)
                token = signatureStage.Sign(payload,time)
                DynamicTokenOperation.UpdateDynamicToken(uuid,token)
                return token
            else:
                print("token tag failed")

        else:
            print("token not exist")
            return None
        
