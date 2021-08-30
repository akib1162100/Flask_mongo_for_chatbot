import sys
sys.path.append("..")
from utils.decorator import token_required
from flask import jsonify, request
from flask_restful import Resource, Api , reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)


class User(Resource):
    @app.route('/user')
    @token_required
    def get_all(current_user):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM users''')
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        rv = cur.fetchall()
        cur.close()
        re_list = []
        for i in range(len(rv)):
            result = dict(zip(field_names, rv[i]))
            print(result)
            re_list.append(result)
        return jsonify(re_list)

    @app.route('/user/<id>')
    @token_required
    def get_by_id(current_user, id):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM users WHERE public_id = %s''', (id,))
        rv = cur.fetchone()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        cur.close()
        result = dict(zip(field_names, rv))
        return jsonify (result)

    @app.route('/user', methods=['POST'])
    @token_required
    def post(current_user):
        user = user_parser.parse_args()
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO users(username, password, public_id) VALUES(%s, %s, %s)''', (user['username'], generate_password_hash(user['password'], method='sha256'), str(uuid.uuid4())))
        mysql.connection.commit()
        cur.close()
        return {'status': 'success'}

    @app.route('/user/<id>', methods=['PUT'])
    @token_required
    def put(current_user,id):
        user = user_parser.parse_args()
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE users SET name = %s, password = %s WHERE public_id = %s''', (user['name'], generate_password_hash(user['password']), id))
        mysql.connection.commit()
        cur.execute('''SELECT * FROM users WHERE public_id = %s''', (id,))
        rv = cur.fetchone()
        num_fields = len(cur.description)
        field_names = [i[0] for i in cur.description]
        cur.close()
        result = dict(zip(field_names, rv))
        return jsonify (result) , 201
        # return {'status': 'success'}

    @app.route('/user/<id>', methods=['DELETE'])
    @token_required
    def delete(current_user,id):
        cur = mysql.connection.cursor()
        cur.execute('''DELETE FROM users WHERE public_id = %s''', (id,))
        mysql.connection.commit()
        cur.close()
        return {'status': 'success'}
