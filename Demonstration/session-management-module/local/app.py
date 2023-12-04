from flask import Flask, request
import jwt
import time

app = Flask(__name__)
def Signing_JWT(payload_data):
    expiration_seconds = 3600
    expiration_time = int(time.time()) + expiration_seconds
    payload_data["exp"] = expiration_time
    payload_data["auth"] = "trigger-service1"
    signed_jwt = jwt.encode(payload_data, "secret", algorithm="HS256")
    return signed_jwt
@app.route('/test', methods=['POST'])
def test_post():
    if request.method == 'POST':
        userID_POST = request.form.get('userID')
        payload_data = {"user_id": userID_POST}
        signed_jwt = Signing_JWT(payload_data)
        return signed_jwt
    else:
        return 'This route only accepts POST requests.'

if __name__ == '__main__':
    app.run(debug=True)
