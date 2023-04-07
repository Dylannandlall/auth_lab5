import requests
import json
import rsa
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#OAUTH_SERVER = "http://192.168.207.34:5001"
OAUTH_SERVER = "http://127.0.0.1:5001"
SECRET_KEY = "abcdefg"

@app.route("/login", methods=['POST'])
def login():

    request_data = request.get_json()

    username = request_data['username']
    password = request_data['password']

    data = {
            'username': username, 
            'password': password
        }
    
    json_data = json.dumps(data)

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    response = requests.post(f"{OAUTH_SERVER}/oauthVerification", data=json_data, headers=headers).json()

    if response["auth"] == "success":
        encrypted_token = encrypt(response["token"], string_kdf(SECRET_KEY))
        json_response = {"auth":"success", "token":encrypted_token}
        json_string = json.dumps(json_response)
        return jsonify(message=(encrypt(json_string, string_kdf(password))))
    
    else:
        return response

    # encrypted_token = (encrypt("This is a token!", string_kdf(SECRET_KEY)))

    # json_response = {"auth":"success", "token":encrypted_token}
    # json_string = json.dumps(json_response)
    # return jsonify(message=(encrypt(json_string, string_kdf(password))))

def encrypt(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message.decode()

def string_kdf(password):
    salt = b'1111'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000)
    
    return base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))


if __name__ == "__main__":
    app.run("localhost", port=5000, debug=True)