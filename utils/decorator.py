from flask import jsonify, request
from functools import wraps
import jwt
import os, sys
sys.path.insert(1, os.getcwd()) 
from app import app , mysql

from flask_restful import Resource, Api , reqparse

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
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users WHERE public_id = %s", [data['public_id']])
            current_user = cursor.fetchone()
            cursor.close()
            # current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated



    

# @app.route('/login')
# def login():
#     auth = request.authorization
#     if not auth or not auth.username or not auth.password:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT * FROM users WHERE username = %s ''', (auth.username,)) 
#     rv = cur.fetchone()
#     cur.close()
#     num_fields = len(cur.description)
#     field_names = [i[0] for i in cur.description]
#     if len(rv) == 0:
#         return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
#     pass_index = field_names.index('password')
#     pid_index = field_names.index('public_id')

#     if check_password_hash(rv[pass_index], auth.password):
#         token = jwt.encode({'public_id': rv[pid_index], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)}, app.config['SECRET_KEY'] ,algorithm="HS256")
#         return jsonify({'token': token})
    
#     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
