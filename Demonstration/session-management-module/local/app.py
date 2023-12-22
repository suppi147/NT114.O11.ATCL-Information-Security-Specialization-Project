from SignOperation import SignOperation
from TokenEncryption import TokenEncryption
from DBinteraction import TokenManager
from flask import Flask, request


def CraftToken(userID_POST):
    payload_data = {"user_id": userID_POST}
    signatureStage = SignOperation()
    cryptoStage = TokenEncryption()
    interactDBStage = TokenManager()
    encryptToken = cryptoStage.Encrypt(signatureStage.Sign(payload_data))
    if not interactDBStage.token_exists(encryptToken):
        if not interactDBStage.uuid_exists(userID_POST):
            interactDBStage.insert_token(encryptToken,userID_POST)
        else:
            print("uuid exist")
    else:
        print("token exist")

def UpdateDynamicToken(userID_POST):
    payload_data = {"user_id": userID_POST}
    signatureStage = SignOperation()
    cryptoStage = TokenEncryption()
    interactDBStage = TokenManager()
    encryptToken = cryptoStage.Encrypt(signatureStage.Sign(payload_data))
    
    if interactDBStage.uuid_exists(userID_POST):
        interactDBStage.update_token(userID_POST,encryptToken)
    else:
        print("uuid not exist")
    

app = Flask(__name__)
@app.route('/token', methods=['POST'])
def test_post():
    app.logger.debug("This is a debug message.")
    if request.method == 'POST':
        userID_POST = request.form.get('userID')
        interactDBStage = TokenManager()
        cryptoStage = TokenEncryption()
        signatureStage = SignOperation()
        
        CraftToken(userID_POST)

        retrieveToken=interactDBStage.get_token_by_uuid(userID_POST)
   
        if not retrieveToken == None:
            decryptToken = cryptoStage.Decrypt(retrieveToken)
            if signatureStage.CheckSignature(decryptToken) == False:
                UpdateDynamicToken(userID_POST)
                retrieveToken = interactDBStage.get_token_by_uuid(userID_POST)
        else:
            print("token is no available acording to uuid "+userID_POST)
        return retrieveToken
    else:
        return 'This route only accepts POST requests.'

if __name__ == '__main__':
    app.run(debug=True)
