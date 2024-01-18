import re

def validate(data, regex):
    # """Custom Validator"""
    return True if re.match(regex, data) else False

def validate_password(password: str):
    # """Password Validator"""
    reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, reg)

def validate_email(Email: str):
    # """Email Validator"""
    # regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # return validate(Email, regex)
    return True

def validate_user(**args):
    # """User Validator"""
    if  not args.get('username') or not args.get('password') or not args.get('email'):
        return {
            'username': 'Username is required',
            'password': 'Password is required',
            'email': 'email is required'
        }
    if not isinstance(args.get('email'), str) or \
        not isinstance(args.get('username'), str) or not isinstance(args.get('password'), str):
        return {
            'username': 'Username must be a string',
            'password': 'Password must be a string',
            'email': 'email must be a string'
        }
    if not validate_email(args.get('email')):
        return {
            'email': 'Email is invalid'
        }
    if not validate_password(args.get('password')):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    # if not 3 <= len(args['key'].split(' ')) <= 30:
    #     return {
    #         'key': 'Key must be between 3 and 30 words'
    #     }
    return True

def validate_email_and_password(username, password):
    # """Email and Password Validator"""
    if not (username and password):
        return {
            'username': 'Username is required',
            'password': 'Password is required'
        }
    if not validate_email(username):
        return {
            'username': 'Username is invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    return True

