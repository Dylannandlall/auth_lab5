import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SECRET_KEY = "abcdefg"

DATA = "You have accessed the secure page of the application server! Here are some quotes from Sun Tzu\n\n1. Appear weak when you are strong, and strong when you are weak.\n2. The supreme art of war is to subdue the enemy without fighting.\n3. If you know the enemy and know yourself, you need not fear the result of a hundred battles. If you know yourself but not the enemy, for every victory gained you will also suffer a defeat. If you know neither the enemy nor yourself, you will succumb in every battle.\n4. Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt.\n"

@app.route("/tokenPage", methods=['POST'])
def tokenPage():

    request_data = request.get_json()

    try:
        auth = request_data['auth']
        token = request_data['token']
    except KeyError:
        print("JSON request not decrypted!")
        return jsonify(status="failed")
        
    decrypted_token = decrypt(token, string_kdf(SECRET_KEY))
    print(decrypted_token)
    return jsonify(status="success", description=DATA)
    


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


if __name__ == "__main__":
    app.run("localhost", port=5002, debug=True)