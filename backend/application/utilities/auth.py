from application.utilities.response import Response
from flask import request
from functools import wraps
import jwt
from config import JWT_SECRETKEY

class Auth:
    def middleware(self, func):
        @wraps(func)
        def decorator():
            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[-1]
            if not token and "Authorization" in request.cookies:
                token=request.cookies.get('Authorization').split(" ")[-1]
            if not token:
                return Response.make(False, 'Unauthorized (Authentication Token is missing!)'), 401
            try:
                jwt.decode(token, JWT_SECRETKEY, algorithms='HS256')
            except jwt.ExpiredSignatureError:
                return Response.make(False, 'Unauthorized'), 401
            except jwt.InvalidTokenError:
                return Response.make(False, 'Invalid token'), 401
            return func()
        return decorator