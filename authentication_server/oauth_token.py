import requests
import json

def get_token():
    headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}

    json_data = {
        'grant_type': 'client_credentials'
    }
    json_data = json.dumps(json_data)
    requests_data = requests.post("http://192.168.207.34:5001", data=json_data, auth=("testclient", "testpass"), headers=headers).json()
    print(requests_data)


if __name__ == "__main__":
    get_token()