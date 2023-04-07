import requests
import json
import subprocess

def get_token():
    user = "testclient"
    password = "testpass"
    url = "http://localhost:8080/token.php"
    type = "grant_type=client_credentials"
    bashCommand = f"curl -u {user}:{password} {url} -d {type}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)

    # headers = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain'}

    # json_data = {
    #     'grant_type': 'client_credentials'
    # }
    # json_data = json.dumps(json_data)
    # requests_data = requests.post("http://192.168.207.34:5001", data=json_data, auth=("testclient", "testpass"), headers=headers)
    # print(requests_data.raise_for_status())


if __name__ == "__main__":
    get_token()