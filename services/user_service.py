import datetime
from flask.json import jsonify
from repository.user_repo import User_repository , User_mongo_repository
import uuid
from app import app
from werkzeug.security import generate_password_hash, check_password_hash
import pytz
import jwt

def make_response(status_code, data, message):
    return jsonify({'status_code': status_code, 'message': message,'data': data})

class User_service():

    def get_user(user_id):
        # message , data , code = User_repository.get_by_id(user_id)        
        message , data , code = User_mongo_repository.get_by_id(user_id)        
        response = make_response(code, data, message)
        return response

    def get_user_data(user_id):
        # user = User_repository.get_by_id(user_id)
        user = User_mongo_repository.get_by_id(user_id)
        print(user)
        response = make_response(200, user, "User data retrieved successfully")
        return response


    def get_all_users():
        # message , data , code = User_repository.get_all()
        message , data , code = User_mongo_repository.get_all()
        response = make_response(code, data, message)
        return response


    def create(user):
        # ids = User_repository.get_all_ids()
        ids = User_mongo_repository.get_all_ids()
        this_uuid = uuid.uuid4().hex
        if this_uuid in ids:
            this_uuid = uuid.uuid4().hex        
        # message , data , code = User_repository.create(this_uuid,user.username,generate_password_hash(user.password , method='sha256'))
        message , data , code = User_mongo_repository.create(this_uuid,user.username,generate_password_hash(user.password , method='sha256'))
        response = make_response(code, data, message)
        return response

    def update_user(id,username,password):
        # message , data , code = User_repository.update(id,username,generate_password_hash(password))
        message , data , code = User_mongo_repository.update(id,username,generate_password_hash(password))
        response = make_response(code, data, message)
        return response

    def delete_user(user_id):
        # message , data , code = User_repository.delete(user_id)
        message , data , code = User_mongo_repository.delete(user_id)
        response = make_response( code, data, message)
        return response


    def user_login(auth):
        print(auth['username'])
        if not auth or not auth['username'] or not auth['password']:
            response = make_response(400, None, "Missing username or password")
            return response
        
        # user = User_repository.get_by_username(auth['username'])
        user = User_mongo_repository.get_by_username(auth['username'])
        if not user:
            response = make_response(400, None, "Could not verify user")
            return response
        
        if check_password_hash(user['password'], auth['password']):
            this_time = datetime.datetime.now(pytz.timezone('Asia/Dhaka'))
            print({'user_id': user['id'], 'exp': this_time+ datetime.timedelta(hours=3)}, app.config['SECRET_KEY'])
            token = jwt.encode({'user_id': user['id'], 'exp': this_time+ datetime.timedelta(hours=3)}, app.config['SECRET_KEY'], algorithm='HS256')
            # User_repository.update_jwt_token(user['id'], token, this_time)
            User_mongo_repository.update_jwt_token(user['id'], token, this_time)
            response = make_response(200, token, "User logged in successfully")
            print(response)
            return response
        response = make_response(400, None, "Could not verify user")
        return response