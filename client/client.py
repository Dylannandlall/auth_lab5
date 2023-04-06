"""
4/6/2023
Author: Dylan Nandlall
OAUTH Client Interface
"""

import sys
import requests
import hashlib
import rsa
import json


# AUTH_SERVER = "192.168.207.33:5000"
AUTH_SERVER = "127.0.0.1:5000"
APP_SERVER = "192.168.207.35:5000"

def login():
    username = input("Please input your username: ")
    password = input("Please input your password: ")
    return username, password

def hash(password):
    return hashlib.sha256(bytes(password, 'utf-8'))

def decrypt(encrypted_message, hashed_password):
    return rsa.decrypt(encrypted_message, hashed_password).decode()

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

        ### Test Loop Code
        # try:
        #     response = requests.post(f"http://{AUTH_SERVER}:5000/login", data, timeout=0.001)
        # except requests.exceptions.ConnectTimeout:
        #     response = {"auth": "fail"}
        response = requests.post(f"http://{AUTH_SERVER}/login", data=json_data, headers=headers)
        print(response.text)

        # if response["auth"] == "fail":
        #     print("Login Credentials are incorrect!")
        #     continue

        # elif response["auth"] == "success":
        #     print("SUCCESS")
        #     # encrypted_token = response["token"]
        #     # decrypted_token = decrypt(encrypted_token, hash(password))
        #     # response = requests.post(f"http://{APP_SERVER}/token")

        # else:
        #     print("ERROR!")
        #     return



def main():
    handler()

if __name__ == "__main__":
    main()