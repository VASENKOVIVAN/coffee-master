
from database_setup import session
from .userModel import User, UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass, asdict
import jwt
import bcrypt
from datetime import datetime, timedelta
from app import app
from flask import request, make_response
from application.utilities.response import Response
from config import JWT_SECRETKEY
from ..utilities.validate import validate_user_request, validate_login_request

class LoginController:
    def login(self):
        """Login user"""
        print('========== LoginController - login ==========')

        is_validated = validate_login_request(**request.json)
        if is_validated is not True:
            return Response.make(False, msg=is_validated), 400

        user=None
        try:
            user=UserController().findUser()
        except LoginErr as msg:
            return Response.make(False, str(msg))
        except Exception as e:
            return Response.make(False, str(e)), 500
        try:
            token=self.createToken(user)
            return self.setCookie(token)
        except Exception as e:
            return Response.make(False, msg='Create token failed (' + str(e) + ')'), 500


    def createToken(self, user):
        payload={
                'exp':datetime.utcnow() + timedelta(minutes=1),
                "iat":datetime.utcnow(),
                'user_id':user._id
            }
        
        token=jwt.encode(
            payload,
            key=JWT_SECRETKEY,
            algorithm='HS256'
            )
        return token


    def setCookie(self, token):
        successLogin={'status':True, 'msg':'Login Success'}
        response=make_response(successLogin)
        response.set_cookie("Authorization", token)
        return response


    def logOut(self):
        resp=make_response({'status':True, 'msg':'Logout Success'})
        resp.delete_cookie('Authorization')
        return resp


class UserController:
    def insertNewData(self):
        """Create a new user"""
        print('========== UserController - insertNewData ==========')

        is_validated = validate_user_request(**request.json)
        if is_validated is not True:
            return Response.make(False, msg=is_validated), 400
        
        parameter={'login':request.json.get('login')}
        user = DataHandler().getUser(parameter)

        if user:
            return Response.make(False, "Conflict (User already exists)"), 409

        try:
            parameter={
                'login':request.json.get('login'),
                'password':bcrypt.hashpw(
                    request.json.get('password').encode('utf-8'), 
                    bcrypt.gensalt()).decode('utf-8'),
                'active': True
            }
            print('UserController.insertNewData.parameter\n', parameter)

            data = DataHandler().insertNewData(parameter)
            print('UserController.insertNewData.data\n', data)

            return Response.make(True, msg='Data successfully added', data=data)
        
        except Exception as e:
            return Response.make(False, msg='Insert data failed (' + str(e) + ')'), 500


    def findUser(self):
        print('========== UserController - findUser ==========')

        parameter={'login':request.json.get('login')}
        user=DataHandler().getUser(parameter)

        if not user:
            raise LoginErr('User is not found')
        if bcrypt.checkpw(request.json.get('password').encode('utf-8'), user.password.encode('utf-8')):
            return user
        raise LoginErr('Permission denied, your password or username is incorrect.')


    def create(self, login="", password=""):
        """Create a new user"""
        user = self.get_by_login(login)
        if user:
            return 0
        newUser = User(login=login, password=self.encrypt_password(password))
        session.add(newUser)  
        session.commit()
        return self.get_by_id(newUser._id)


    def get_by_id(self, user_id):
        """Get a user by id"""
        user = session.query(User).filter_by(_id=user_id).one()
        return user


    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)
    

    def get_by_login(self, login):
        """Get a user by login"""
        user = session.query(User).filter_by(login=login).all()
        # user = db.users.find_one({"login": login, "active": True})
        return user


    def user_login(self, login, password):
        """Login a user"""
        print(login)
        print(password)

        user = self.get_by_login(login)
        print(user.password)
        if not check_password_hash(user.password, password):
            return 
        return user


    # def get_all(self):
    #     """Get all users"""
    #     users = db.users.find({"active": True})
    #     return [{**user, "_id": str(user["_id"])} for user in users]


    # def update(self, user_id, name=""):
    #     """Update a user"""
    #     data = {}
    #     if name:
    #         data["name"] = name
    #     user = db.users.update_one(
    #         {"_id": bson.ObjectId(user_id)},
    #         {
    #             "$set": data
    #         }
    #     )
    #     user = self.get_by_id(user_id)
    #     return user


    # def delete(self, user_id):
    #     """Delete a user"""
    #     Books().delete_by_user_id(user_id)
    #     user = db.users.delete_one({"_id": bson.ObjectId(user_id)})
    #     user = self.get_by_id(user_id)
    #     return user

    # def disable_account(self, user_id):
        """Disable a user account"""
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {"$set": {"active": False}}
        )
        user = self.get_by_id(user_id)
        return user


class DataHandler:
    def __init__(self):
        self.Model=User
        self.Schema=UserSchema
    

    def getUser(self, parameter):
        """Get a user by id"""
        print('========== DataHandler - getUser ==========')

        try:
            data = session.query(User).filter_by(
                    login=parameter['login'], 
                    active=True
                ).first()
            return data

        except Exception as e:
            return Response.make(False, str(e)), 500

     
    def insertNewData(self, parameter):
        print('========== DataHandler - insertNewData ==========')

        # objectToInsert=User(**parameter)
        # db.session.add(objectToInsert)
        # db.session.commit()
        objectToInsert=self.Model(**parameter)
        # objectToInsert = User(**parameter)
        print('DataHandler.insertNewData.objectToInsert', objectToInsert)
        session.add(objectToInsert)  
        session.commit()
        return self.Schema().dump(objectToInsert)
        # return objectToInsert


class LoginErr(Exception):
    """Custom Exception for login error"""