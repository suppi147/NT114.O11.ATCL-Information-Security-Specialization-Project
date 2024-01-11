from cryptography.hazmat.backends import openssl
from cryptography.hazmat.primitives import hashes

def sha3_256(data):
    backend = openssl.backend
    digest = hashes.Hash(hashes.SHA3_256(), backend=backend)
    digest.update(data.encode('utf-8'))
    hashed_data = digest.finalize()
    return hashed_data.hex()

