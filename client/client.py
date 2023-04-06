"""
4/6/2023
Author: Dylan Nandlall
OAUTH Client Interface
"""

import sys
import requests
import hashlib
import rsa


AUTH_SERVER = "192.168.207.33"
APP_SERVER = "192.168.207.35"

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

        data = {'username': username, 'password': password}

        ### Test Loop Code
        # try:
        #     response = requests.post(f"http://{AUTH_SERVER}:5000/login", data, timeout=0.001)
        # except requests.exceptions.ConnectTimeout:
        #     response = {"auth": "fail"}
        response = requests.post(f"http://{AUTH_SERVER}:5000/login", data)

        if response["auth"] == "fail":
            print("Login Credentials are incorrect!")
            continue

        elif response["auth"] == "success":
            encrypted_token = response["token"]
            decrypted_token = decrypt(encrypted_token, hash(password))
            response = requests.post(f"http://{APP_SERVER}/token")

        else:
            print("ERROR!")
            return



def main():
    handler()

if __name__ == "__main__":
    main()