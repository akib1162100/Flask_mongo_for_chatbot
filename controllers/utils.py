from flask import request , jsonify
from functools import wraps
import jwt
from app import app
from services.user_service import User_service


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Access-Tocken' in request.headers:
            token = request.headers['X-Access-Tocken']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user = User_service.get_user(data['user_id'])

        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated