from SignOperation import SignOperation
from TokenEncryption import TokenEncryption
from flask import Flask, request
from time import sleep
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
@app.route('/test', methods=['POST'])
def test_post():
    app.logger.debug("This is a debug message.")
    if request.method == 'POST':
        userID_POST = request.form.get('userID')
        payload_data = {"user_id": userID_POST}
        a = SignOperation()
        b = TokenEncryption()
        final = b.Decrypt(b.Encrypt(a.Sign(payload_data)))
        print(a.CheckSignature(final))
        sleep(10)
        print(a.CheckSignature(final))
        return 'token has been created'
    else:
        return 'This route only accepts POST requests.'

if __name__ == '__main__':
    app.run(debug=True)
