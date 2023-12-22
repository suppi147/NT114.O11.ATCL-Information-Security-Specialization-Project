# Your corrected JWT token
jwt_token = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjdmMzA5M2UtZjM1Yy00YzU4LWJfMDktZjNkMDc5MTQ3ZTIyIiwiZXhwIjoxNzAzMjU0MTkzLCJhdXRoLXNlcnZpY2UiOiJ0cmlnZ2VyLXNlcnZpY2UxIn0.nBhtyhyqpGXoae5ZVadHymtoyH6YotPmo35rfFPdRv3-djoXvEqB_CiRdXSVuR6rL9HLjz4ALTQ61bWWxdnnSQ.7o4Y+Ebj4Ok7PdtwXSuC8UG72523L4SODZEWzuRep9o="

# Split the JWT token into its parts
token_parts = jwt_token.split('.')

# Extract the base64 tag after the last dot
last_base64_tag = token_parts[-1]

print("\nBase64 Tag after the Last Dot:", last_base64_tag)
