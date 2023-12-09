from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import os
import hashlib
import base64
from base64 import urlsafe_b64encode, urlsafe_b64decode
class TokenEncryption():
    secret = None
    key = None
    nonce = None
    encryptToken = None
    token = None
    salt = None
    @staticmethod
    def GetSecretFromTPM():
        hexSecret=os.environ.get('CRYPTO_KEY')
        byte_data = bytes.fromhex(hexSecret)
        TokenEncryption.secret = base64.b64encode(byte_data).decode('utf-8')
        print("Encryption secret has been retreived.")
    @staticmethod
    def derive_key_from_passphrase(passphrase):
        salt = b''
        TokenEncryption.key = hashlib.pbkdf2_hmac('sha256', passphrase.encode('utf-8'), salt, iterations=100000, dklen=32)
        
    def Encrypt(self,signedToken):
        byteSignedToken = signedToken.encode()
        self.GetSecretFromTPM()
        if TokenEncryption.secret != None:
            self.derive_key_from_passphrase(TokenEncryption.secret)
            TokenEncryption.nonce = os.urandom(12)
            cipher = AESGCM(TokenEncryption.key)
            ciphertext = cipher.encrypt(TokenEncryption.nonce, byteSignedToken, None)
            TokenEncryption.encryptToken = urlsafe_b64encode(TokenEncryption.nonce + ciphertext)
            TokenEncryption.encryptToken = TokenEncryption.encryptToken.decode()
            print("Encryption token completed: " + TokenEncryption.encryptToken)
            return TokenEncryption.encryptToken
        else:
            print("Encryption secret has not been retreived.")
    def Decrypt(self,encryptedToken):
        self.GetSecretFromTPM()
        if TokenEncryption.secret != None:
            self.derive_key_from_passphrase(TokenEncryption.secret)
            cipher = AESGCM(TokenEncryption.key)
            TokenEncryption.encryptToken = urlsafe_b64decode(encryptedToken)
            TokenEncryption.nonce = TokenEncryption.encryptToken[:12]
            TokenEncryption.encryptToken = TokenEncryption.encryptToken[12:]
            TokenEncryption.token = cipher.decrypt(TokenEncryption.nonce, TokenEncryption.encryptToken, None)
            TokenEncryption.token = TokenEncryption.token.decode()
            print("Decryption token completed: " + TokenEncryption.token)
            return TokenEncryption.token
        else:
            print("Encryption secret has not been retreived.")