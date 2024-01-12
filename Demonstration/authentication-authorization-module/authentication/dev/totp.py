import pyotp
import aes
from DBInteraction import AuthManager

def totp(username):
    interactDBStage = AuthManager()
    totpkey = interactDBStage.get_totpkey_by_username(username)
    if totpkey is not None:
        key = aes.decrypt_aes_cbc(totpkey)
        totp = pyotp.TOTP(key)
        otp = totp.now()
        return otp
    else:
        return None