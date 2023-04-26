from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/api/v1/message', methods=['GET'])
def message():
    return jsonify(
        message="Automate all the things!",
        timestamp=int(time.time())
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
