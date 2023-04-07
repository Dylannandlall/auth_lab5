"""
4/6/2023
Author: Dylan Nandlall
OAUTH Client Interface
"""

import requests
import base64
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet



AUTH_SERVER = "192.168.207.33:5000"
# AUTH_SERVER = "127.0.0.1:5000"
APP_SERVER = "192.168.207.35:5002"
# APP_SERVER = "127.0.0.1:5002"

def handler():
    print("This is a demonstration of our OAUTH implementation!\n")
    
    while True:
        username, password = login()

        data = {
            'username': username, 
            'password': password
        }
        json_data = json.dumps(data)

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}


        response = (requests.post(f"http://{AUTH_SERVER}/login", data=json_data, headers=headers)).json()
        # print(response["message"])

        encrypted_message = response["message"]
        decrypted_response = (decrypt(encrypted_message, string_kdf(password))).decode()
        decrypted_response = json.loads(decrypted_response)
        print(decrypted_response)

    
        # decrypted_response = json.loads(decrypted_response)
        # encrypted_message2 = decrypted_response["token"]
        # decrypted_response2 = (decrypt(encrypted_message2, password_kdf("abcdefg"))).decode()
        # print(decrypted_response2)


        if decrypted_response["auth"] == "fail":
            print("Login Credentials are incorrect!")
            continue

        elif decrypted_response["auth"] == "success":
            print("SUCCESS")
            data = {
                "auth" : decrypted_response["auth"],
                "token" : decrypted_response["token"]
            }

            json_data = json.dumps(data)
            response = requests.post(f"http://{APP_SERVER}/tokenPage", data=json_data, headers=headers).json()

            if response["status"] == "success":
                print(response["description"])
                return
            

        else:
            print("ERROR!")
            return

def login():
    username = input("Please input your username: ")
    password = input("Please input your password: ")
    return username, password

def string_kdf(password):
    salt = b'1111'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000)
    
    return base64.urlsafe_b64encode(kdf.derive(bytes(password, 'utf-8')))

def decrypt(encrypted_message, key):
    encrypted_message = encrypted_message.encode()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message)

def main():
    handler()

if __name__ == "__main__":
    main()