from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib
import os

rootkey = os.environ.get('authen_totp_secret_key')
def encrypt_aes_cbc(data):
    secretkey=rootkey
    key = hashlib.sha256(secretkey.encode()).digest()
    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()

    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    encrypted_message = urlsafe_b64encode(iv + cipher_text).decode('utf-8')

    return encrypted_message

def decrypt_aes_cbc(cipher_text):
    secretkey=rootkey
    key = hashlib.sha256(secretkey.encode()).digest()
    decoded_cipher_text = urlsafe_b64decode(cipher_text)

    iv = decoded_cipher_text[:16]
    cipher_text = decoded_cipher_text[16:]

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(decrypted_data) + unpadder.finalize()

    return data.decode('utf-8')

