import jwt
token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyX2lkIjoiOWE0MDU5MTAtYjkwMC00MTc5LWEyMjgtNGQyMmRiMGUwMWMxIiwiZmluZ2VycHJpbnQiOiJkMzhjZmFiYjZjZDk1YzcxM2IyMDFhOTFmMjhhZjMwZCIsImF1dGgtc2VydmljZSI6IlF1b3RlU2VydmljZV8iLCJleHAiOjE3MDUxNzE2OTd9.jm139bxQIthn6Bk1+LmwGR/eNozaATJHDflYhitlbLw"
token_parts = token.split('.')
last_base64_tag = token_parts[2]
token_without_tag = token_parts[0]+"."+token_parts[1]+"."
print("token_without_tag:",token_without_tag)
print("last_base64_tag:",last_base64_tag)
payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
print(payload_data)