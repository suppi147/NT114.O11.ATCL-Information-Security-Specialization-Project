from flask import Flask
app = Flask(__name__)

@app.route('/bar')
def hello():
    return '{"msg":"Hello from the bar microservice"}'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')