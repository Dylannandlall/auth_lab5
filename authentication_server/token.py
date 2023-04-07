import requests
import json

def get_token():
    json_data = {
        'grant_type': 'client_credentials'
    }
    requests_data = requests.post("http://192.168.207.34:5001", data=json_data, auth=("testclient", "testpass")).json()
    print(requests_data)


if __name__ == "__main__":
    get_token()