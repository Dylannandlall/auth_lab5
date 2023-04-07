from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SECRET_KEY = "abcdefg"

@app.route("/oauthVerification", methods=['POST'])
def oauthVerification():

    request_data = request.get_json()
    
    username = request_data['username']
    password = request_data['password']

    if validate_credentials(username, password) == True:
        return jsonify(auth="success", token="this is a token lol")
    else:
        return jsonify(auth="fail", token="")


def validate_credentials(username, password):
    return True

if __name__ == "__main__":
    app.run("192.168.207.34", port=5001, debug=True)