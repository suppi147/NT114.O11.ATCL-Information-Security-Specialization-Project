from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/get_epoch_time', methods=['GET'])
def get_epoch_time():
    current_time = int(time.time())
    return jsonify({'epoch_time': current_time})

if __name__ == '__main__':
    app.run(debug=True)
