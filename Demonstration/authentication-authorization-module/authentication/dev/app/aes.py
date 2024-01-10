from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def encrypt_aes_cbc(data, key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(hashlib.sha256(key.encode()).digest(), AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(data.encode()))
    return base64.b64encode(iv + cipher_text).decode('utf-8')

def pad(s):
    block_size = AES.block_size
    padding_length = block_size - len(s) % block_size
    padding = bytes([padding_length] * padding_length)
    return s + padding


def decrypt_aes_cbc(cipher_text, key):
    decoded_cipher_text = base64.b64decode(cipher_text)
    iv = decoded_cipher_text[:AES.block_size]
    cipher = AES.new(hashlib.sha256(key.encode()).digest(), AES.MODE_CBC, iv)
    decrypted_text = unpad(cipher.decrypt(decoded_cipher_text[AES.block_size:]))
    return decrypted_text.decode('utf-8')

def unpad(s):
    padding_length = s[-1]
    return s[:-padding_length]

