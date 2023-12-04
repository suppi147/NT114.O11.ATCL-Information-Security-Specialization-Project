from flask import Flask, request
import jwt

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test_post():
    if request.method == 'POST':
        data = request.form.get('user')
        encoded_jwt = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
        return encoded_jwt
    else:
        return 'This route only accepts POST requests.'

if __name__ == '__main__':
    app.run(debug=True)
