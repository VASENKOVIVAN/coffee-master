import bcrypt
import jwt, os
from flask import Flask, jsonify, request, make_response
from config import host, user, password, db_name
import mysql.connector
# from database_setup import Book, User
from application.user.userController import UserController, LoginController

from auth_middleware import token_required
from validate import validate_book, validate_user
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

# JWT_SECRETKEY=bcrypt.hashpw(b'itsAs3cr34tkeyforJWT', bcrypt.gensalt())

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def hello_world():
    return "<h1>Hello, World!<h1>"


@app.post('/newuser')
def newUser():
    return UserController().insertNewData()


@app.route("/users/", methods=["POST"])
def add_user():
    try:
        user = dict(request.get_json())
        
        # user_check = User().get_by_login(user['login'])
        is_validated = validate_user(**user)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        
        user = UserController().create(**user)

        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409

        _dict = user.__dict__.copy()
        _dict['_id'] = str(_dict['_id'])
        _dict.pop('password')
        _dict.pop('_sa_instance_state')


        return {
            "message": "Successfully created new user",
            "data": _dict
        }, 201

    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500
    


# @app.route("/users/", methods=["POST"])
# def add_user():
#     try:
#         user = dict(request.get_json())
        
#         user_check = User().get_by_login(user['login'])
#         if len(user_check) == 0:
#             user = User().create(**user)
#             _dict = user.__dict__.copy()
#             _dict['_id'] = str(_dict['_id'])
#             _dict.pop('password')
#             _dict.pop('_sa_instance_state')

#             return {
#                 "message": "Successfully created new user",
#                 "data": _dict
#             }, 201
#         else:
#             return {
#                     "message": "User already exists",
#                     "error": "Conflict",
#                     "data": None
#                 }, 409
#     except Exception as e:
#         return {
#             "message": "Something went wrong",
#             "error": str(e),
#             "data": None
#         }, 500


# Эта функция позволит создать новую книгу и сохранить ее в базе данных.
# @app.route('/books/new/', methods=['POST'])
# @token_required
# def add_book(current_user):
#     try:
#         book = dict(request.get_json())

#         is_validated = validate_book(**book)
#         if is_validated is not True:
#             return {
#                 "message": "Invalid data",
#                 "data": None,
#                 "error": is_validated
#             }, 400

#         book = Book().create(**book)

#         if not book:
#             return {
#                 "message": "The book has been created by user",
#                 "data": None,
#                 "error": "Conflict"
#             }, 400
#         return jsonify({
#             "message": "successfully created a new book",
#             "data": book
#         }), 201
#     except Exception as e:
#         return jsonify({
#             "message": "failed to create a new book",
#             "error": str(e),
#             "data": None
#         }), 500


@app.post('/login')
def login():
    return LoginController().login()


# @app.route("/users/login", methods=["POST"])
# def login():
#     try:
#         data = dict(request.get_json())
#         if not data:
#             return {
#                 "message": "Please provide user details",
#                 "data": None,
#                 "error": "Bad request"
#             }, 400
        
#         print(data)
#         # validate input
#         # is_validated = validate_email_and_password(data.get('email'), data.get('password'))
#         # if is_validated is not True:
#         #     return dict(message='Invalid data', data=None, error=is_validated), 400
#         user = UserController().user_login(
#             data["login"],
#             data["password"]
#         )
#         print('vsdsvsdd')
#         if user:
#             try:
#                 # print(user.token)
#                 # token should expire after 24 hrs
#                 # user["token"] = jwt.encode(
#                 #     {"user_id": user["_id"]},
#                 #     app.config["SECRET_KEY"],
#                 #     algorithm="HS256"
#                 # )
#                 now = datetime.now(timezone.utc)
#                 token_age_h = 0
#                 token_age_m = 1
#                 expire = now + timedelta(hours=token_age_h, minutes=token_age_m)
#                 payload = dict(exp=expire, iat=now, user_id=user._id)

#                 token = jwt.encode(
#                     # {"user_id": user._id},
#                     payload,
#                     app.config["SECRET_KEY"],
#                     algorithm="HS256"
#                 )
#                 return {
#                     "message": "Successfully fetched auth token",
#                     "data": token
#                 }
#             except Exception as e:
#                 return {
#                     "error": "Something went wrong",
#                     "message": str(e)
#                 }, 500
#         return {
#             "message": "Error fetching auth token!, invalid email or password",
#             "data": None,
#             "error": "Unauthorized"
#         }, 404
#     except Exception as e:
#         return {
#                 "message": "Something went wrong!",
#                 "error": str(e),
#                 "data": None
#         }, 500



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
