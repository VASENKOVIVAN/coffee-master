"""Validator Module"""
import re

def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False


def validate_user_request(**args):
    """User Request Validator"""
    if not args:
        return "Bad request (Please provide user details)"
    if not args.get('login') or not args.get('password'):
        return {
            'login': 'Login is required',
            'password': 'Password is required'
        }
    if not isinstance(args.get('login'), str) or not isinstance(args.get('password'), str):
        return {
            'login': 'Login must be a string',
            'password': 'Password must be a string'
        }
    if not validate_login(args.get('login')):
        return {
            'login': 'Login is invalid, Should be 3-20 characters'
        }
    if not validate_password(args.get('password')):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with upper and lower case letters, numbers and special characters'
        }
    return True


def validate_login_request(**args):
    """Login Request Validator"""
    if not args:
        return "Bad request (Please provide user details)"
    if not args.get('login') or not args.get('password'):
        return {
            'login': 'Login is required',
            'password': 'Password is required'
        }
    return True


def validate_book(**args):
    """Book Validator"""
    if not args.get('title') or not args.get('genre') \
        or not args.get('author'):
        return {
            'title': 'Title is required',
            'genre': 'Genre is required',
            'author': 'Author is required'
        }

    if not isinstance(args.get('title'), str) or not isinstance(args.get('genre'), str) \
        or not isinstance(args.get('author'), str):
        return {
            'title': 'Title must be a string',
            'genre': 'Genre must be a string',
            'author': 'Author must be a string'
        }
    return True


def validate_password(password: str):
    """Password Validator"""
    reg = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    return validate(password, reg)


def validate_login(login: str):
    """Login Validator"""
    print('loginloginloginlogin', login)
    regex = r"^.{3,20}$"
    return validate(login, regex)

