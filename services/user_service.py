import datetime
from flask.json import jsonify
from repository.user_repo import User_repository
import uuid
from app import app
from models.user import User
from models.response import Response
from werkzeug.security import generate_password_hash, check_password_hash
import pytz
import jwt

class User_service():
    # user_repo = User_repository()
    # user = User()
    # response = Response()

    # def __init__(self):
    #     self.user_repo = User_repository()
    #     self.user = User()
    #     self.response = Response()

    def get_user(user_id):
        message , data , code = User_repository.get_by_id(user_id)        
        response = Response(code, data, message)
        return response

    def get_user_data(user_id):
        user = User_repository.get_by_id(user_id)
        response = Response(200, user, "User data retrieved successfully")
        return response


    def get_all_users():
        message , data , code = User_repository.get_all()
        response = Response(code, data, message)
        return response


    def create(user):
        ids = User_repository.get_all_ids()
        this_uuid = uuid.uuid4().hex
        if this_uuid in ids:
            this_uuid = uuid.uuid4().hex        
        message , data , code = User_repository.create(this_uuid,user.username,generate_password_hash(user.password , method='sha256'))
        response = Response(code, data, message)
        return response

    def update_user(id,username,password):
        message , data , code = User_repository.update(id,username,generate_password_hash(password))
        response = Response(code, data, message)
        return response

    def delete_user(user_id):
        message , data , code = User_repository.delete(user_id)
        response = Response( code, data, message)
        return response


    def user_login(auth):
        print(auth['username'])
        if not auth or not auth['username'] or not auth['password']:
            response = Response(400, None, "Missing username or password")
            return response
        
        user = User_repository.get_by_username(auth['username'])
        print(user['username'])
        if not user:
            response = Response(400, None, "Could not verify user")
            return response

        if check_password_hash(user['password'], auth['password']):
            this_time = datetime.datetime.now(pytz.timezone('Asia/Dhaka'))
            token = jwt.encode({'user_id': user['id'], 'exp': this_time+ datetime.timedelta(hours=3)}, app.config['SECRET_KEY'], algorithm='HS256')
            User_repository.update_jwt_token(user['id'], token, this_time)
            response = Response(200, token, "User logged in successfully")
            return response
        response = Response(400, None, "Could not verify user")
        return response