from flask import Flask, request, make_response, render_template, jsonify

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def view_log():
    return "test",200

if __name__ == '__main__':
    app.run(debug=True)
