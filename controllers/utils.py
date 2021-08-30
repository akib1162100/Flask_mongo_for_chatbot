from flask import request , jsonify
from functools import wraps
import jwt
from app import app
from services.user_service import User_service


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            print(token)
            print()
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            print(data)
            current_user = User_service.get_user_data(data['user_id'])
            print(current_user)

        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated