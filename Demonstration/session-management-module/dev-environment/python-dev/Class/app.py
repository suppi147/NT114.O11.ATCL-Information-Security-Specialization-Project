from flask import Flask, request, make_response, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/check', methods=['GET'])
def check():
    data = request.json
    token = data.get('token')
    service = data.get('service')
    
    return "test",200

if __name__ == '__main__':
    app.run(debug=True)
