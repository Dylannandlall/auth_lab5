from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/login", methods=['POST'])
def login():

    request_data = request.get_json()

    username = request_data['username']
    password = request_data['password']

    return jsonify(auth="success")

if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)