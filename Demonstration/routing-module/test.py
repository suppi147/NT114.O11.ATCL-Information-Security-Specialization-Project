import jwt

def export_result_to_file(result, file_path):
    try:
        with open(file_path, 'w') as file:
            print(result, file=file)
        print(f"Result exported to {file_path}")
    except Exception as e:
        print(f"Error exporting result to {file_path}: {e}")

token = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyX2lkIjoiMGNiNzc3YzgtYWE5ZC00ZTUyLTg3ZDAtOTYwOTc1ZGJjOTc0IiwiZmluZ2VycHJpbnQiOiIwZDAyMzAxNWMwZTE3MTRmYWJmNDgwZDNmNjFiMjM3ZCIsImF1dGgtc2VydmljZSI6IlF1b3RlU2VydmljZV8iLCJleHAiOjE3MDU1OTc3MTF9.bkcSlTvqsoFd18mJkq+pvGZxbVE30rvFtdHwiz1UR/M="
token_parts = token.split('.')
last_base64_tag = token_parts[2]
token_without_tag = token_parts[0]+"."+token_parts[1]+"."
print("token_without_tag:",token_without_tag)
print("last_base64_tag:",last_base64_tag)
payload_data = jwt.decode(token_without_tag, options={"verify_signature": False})
print(payload_data)
export_result_to_file(payload_data,"D:\\Github\\NT114.O11.ATCL-Information-Security-Specialization-Project\\Demonstration\\routing-module\\a.txt")