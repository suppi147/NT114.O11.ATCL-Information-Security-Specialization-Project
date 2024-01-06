from functools import wraps
import jwt
from flask import request, abort
import model

SECRET_KEY = 'toan'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        # token = None
        # if "Authorization" in request.headers:
        #     token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = model.get_by_id(data["user_id"])
            # current_user = model.get_user(username['username'])
            # current_user=model.get_by_id(data["user_id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(data, *args, **kwargs)

    return decorated

