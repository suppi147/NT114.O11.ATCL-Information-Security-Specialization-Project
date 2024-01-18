import jwt
token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyX2lkIjoiOGUxOWE3YzEtNjM2Ny00MTdlLWFjNTItNzAzYmQ3ZTRiM2U4IiwiZmluZ2VycHJpbnQiOiJOVUxMIiwiYXV0aC1zZXJ2aWNlIjoiUXVvdGVTZXJ2aWNlXyIsImV4cCI6MTcwNTU1NTg3Mn0.oys0j8zzMjQCSC3gIm4WlkpQLJL9TWmVxjcFxtvvk08="
token_parts = token.split('.')
last_base64_tag = token_parts[2]
token_without_tag = token_parts[0]+"."+token_parts[1]+"."
print("token_without_tag:",token_without_tag)
print("last_base64_tag:",last_base64_tag)
payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
print(payload_data)