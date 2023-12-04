from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import hashlib
from base64 import urlsafe_b64encode, urlsafe_b64decode

def encrypt(plaintext, key):
    # Generate a random 96-bit nonce
    nonce = os.urandom(12)

    # Create AES-GCM cipher with the provided key
    cipher = AESGCM(key)

    # Encrypt the plaintext
    ciphertext = cipher.encrypt(nonce, plaintext, None)

    # Return the nonce and ciphertext as a base64-encoded string
    return urlsafe_b64encode(nonce + ciphertext)

def decrypt(ciphertext, key):
    # Decode the base64-encoded string to get the nonce and ciphertext
    data = urlsafe_b64decode(ciphertext)

    # Extract the nonce and ciphertext
    nonce = data[:12]
    ciphertext = data[12:]

    # Create AES-GCM cipher with the provided key
    cipher = AESGCM(key)

    # Decrypt the ciphertext
    plaintext = cipher.decrypt(nonce, ciphertext, None)

    # Return the decrypted plaintext
    return plaintext
def derive_key_from_passphrase(passphrase,salt):
    # Derive a 256-bit key using SHA-256
    key = hashlib.pbkdf2_hmac('sha256', passphrase.encode('utf-8'), salt, iterations=100000, dklen=32)
    return key
# Example usage
passphrase = "your_32_byte_key_for_AES256_GCM"
salt = os.urandom(16)
key = derive_key_from_passphrase(passphrase,salt)
plaintext = b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsImV4cCI6MTcwMTcwMTM5OSwiYXV0aCI6InRyaWdnZXItc2VydmljZTEifQ.agiag2gCsdJF3RDoTXQxtxmJVkejNSjejgMou41-ngI'
ciphertext = encrypt(plaintext, key)

print(f'Plaintext: {plaintext.decode()}')
print(f'Ciphertext: {ciphertext}')

decrypted_text = decrypt(ciphertext, key)
print(f'Decrypted Text: {decrypted_text.decode()}')
