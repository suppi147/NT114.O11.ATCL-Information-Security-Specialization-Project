import requests

url = 'http://session-management-service/test'  # Thay đổi địa chỉ nếu cần

# Dữ liệu để gửi trong POST request
data = {'userID': 1}  # Thay đổi giá trị của input_string nếu cần

# Gửi POST request
response = requests.post(url, data=data)

# In ra kết quả
print(response.text)
