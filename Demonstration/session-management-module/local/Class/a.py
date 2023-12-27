import jwt
from datetime import datetime, timedelta

# Payload (claims)
payload_data = {"user_id": "userID_POST"}
payload_data["fingerprint"] = "8db79807430561f22709adb678ddfd3a"
payload_data["auth-service"] = "trigger-service1"
payload_data["exp"] = datetime.utcnow() + timedelta(seconds=5)

# Create unsigned JWT
unsigned_token = jwt.encode(payload_data, key=None,algorithm=None)


payload_data = jwt.decode(unsigned_token, options={"verify_signature": False})

expiration_time = payload_data.get("exp")

if expiration_time:
    expiration_datetime = datetime.utcfromtimestamp(expiration_time)
    current_datetime = datetime.utcnow()

    if current_datetime < expiration_datetime:
        print("Token is not expired.")
    else:
        print("Token has expired.")
else:
    print("Token does not contain an expiration time.")    


print("Unsigned JWT:", unsigned_token)

print("payload_data[fingerprint]:", payload_data["fingerprint"])