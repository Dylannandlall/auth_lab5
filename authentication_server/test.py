
import base64
import json
import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


def main():
    # publicKey, privateKey = rsa.newkeys(512)
    publicKey = "hello"

    message = { "name":"John", "age":30, "city":"New York"}
    message = json.dumps(message)
    
    salt = b"1111"

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000)
    
    key = base64.urlsafe_b64encode(kdf.derive(bytes(publicKey, 'utf-8')))
    # key = kdf.derive(b"password")

    salt = b"1111"
    kdf2 = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000)
    
    try:
        kdf2.verify((bytes(publicKey, 'utf-8')), base64.urlsafe_b64decode(key))
    except cryptography.exceptions.InvalidKey:
        print("Key is not Valid!")
    else:
        print("Key is valid!")

    fernet = Fernet(key)


    encrypted_message = fernet.encrypt(message.encode())
    print(encrypted_message.decode())
    # string_encrypted_message = base64.encodebytes(encrypted_message)
    # # print(encrypted_message)
    # print(string_encrypted_message)
    # string_encrypted_message = string_encrypted_message.decode()
    # print(string_encrypted_message)
    # string_encrypted_message = string_encrypted_message.encode()
    # print(string_encrypted_message)
    # # if encrypted_message == base64.decodebytes(string_encrypted_message):
    # #     print("True!")
if __name__ == "__main__":
    main()