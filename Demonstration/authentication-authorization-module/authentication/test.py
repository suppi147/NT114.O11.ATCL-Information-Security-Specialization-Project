import pyotp

def a():
    return pyotp.random_base32()

def b(key):
    return pyotp.totp.TOTP(key).provisioning_uri(name='toan')

a = a()
print(a)

u = b(a)
print(u)
