import requests
import json
import base64
import subprocess
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

OAUTH_SERVER = "http://192.168.207.34:5001"
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
    
    # json_data = json.dumps(data)

    # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    # response = requests.post(f"{OAUTH_SERVER}/oauthVerification", data=json_data, headers=headers).json()

    response = get_token(username, password)

    try:
        if response["access_token"] != "":
            encrypted_token = encrypt(response["access_token"], string_kdf(SECRET_KEY))
            json_response = {"auth":"success", "token":encrypted_token}
            json_string = json.dumps(json_response)
            return jsonify(message=(encrypt(json_string, string_kdf(password))))
    except requests.exceptions.JSONDecodeError:
        json_response = {"auth":"fail", "token":""}
        json_string = json.dumps(json_response)
        return jsonify(message=(encrypt(json_string, string_kdf(password))))
    else:
        json_response = {"auth":"fail", "token":""}
        json_string = json.dumps(json_response)
        return jsonify(message=(encrypt(json_string, string_kdf(password))))

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

def get_token(username, password):
    url = "http://192.168.207.34:8080/token.php"
    type = "grant_type=client_credentials"
    bashCommand = f"curl -u {username}:{password} {url} -d {type}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    response = output.decode()
    response_json = json.loads(output)
    return(response_json)


if __name__ == "__main__":
    app.run("192.168.207.33", port=5000, debug=True)