import requests
import json
import subprocess

def get_token():
    user = "testclient"
    password = "testpass"
    url = "http://192.168.207.34:8080/token.php"
    type = "grant_type=client_credentials"
    bashCommand = f"curl -u {user}:{password} {url} -d {type}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    # print(output.decode())
    response = output.decode()
    response_json = json.loads(output)
    print(response_json["access_token"])


if __name__ == "__main__":
    get_token()