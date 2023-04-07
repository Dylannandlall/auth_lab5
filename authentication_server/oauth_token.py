import requests
import json
import subprocess

def get_token():
    user = "testclient"
    password = "testpass"
    url = "http://localhost:8080/token.php"


    bashCommand = f"curl -u {user}:{password} {url} -d 'grant_type=client_credentials'"
    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output)
   

if __name__ == "__main__":
    get_token()