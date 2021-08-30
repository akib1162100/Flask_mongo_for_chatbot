from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_restful import Resource, Api , reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import yaml
import uuid
import jwt
import datetime
import pytz 


db = yaml.load(open('db.yml'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'soft@2019'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['MYSQL_HOST']= db['mysql_host']
app.config['MYSQL_USER']= db['mysql_user']
app.config['MYSQL_PASSWORD']= db['mysql_password']
app.config['MYSQL_DB']= db['mysql_database']

mysql = MySQL(app)

api = Api(app)

class Helloworld(Resource):
    def get(self):
        return {'data':'Hello world'}

api.add_resource(Helloworld, '/hello')


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
            cursor.execute("SELECT * FROM users WHERE id = %s", [data['id']])
            current_user = cursor.fetchone()
            print(current_user)
            cursor.close()
            # current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True)
user_parser.add_argument('password', type=str, required=True)


class User(Resource):
    @app.route('/user')
    @token_required
    def get_all(current_user):
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM users''')
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
        cur.execute('''SELECT * FROM users WHERE id = %s''', (id,))
        rv = cur.fetchone()
        field_names = [i[0] for i in cur.description]
        cur.close()
        result = dict(zip(field_names, rv))
        return jsonify (result)

    @app.route('/user', methods=['POST'])
    @token_required
    def post(current_user):
        user = user_parser.parse_args()
        cur = mysql.connection.cursor()
        cur.execute('''SELECT id FROM users''')
        uuids = cur.fetchall()
        uuid_list = []
        for i in range(len(uuids)):
            uuid_list.append(uuids[i][0])
        print(uuid_list)
        this_uuid = uuid.uuid4().hex
        if this_uuid in uuid_list:
            this_uuid = uuid.uuid4().hex
        cur.execute('''INSERT INTO users(username, password, id) VALUES(%s, %s, %s)''', (user['username'], generate_password_hash(user['password'], method='sha256'), str(this_uuid)))
        mysql.connection.commit()
        cur.close()
        return {'status': 'success'}

    @app.route('/user/<id>', methods=['PUT'])
    @token_required
    def put(current_user,id):
        user = user_parser.parse_args()
        cur = mysql.connection.cursor()
        cur.execute('''UPDATE users SET name = %s, password = %s WHERE id = %s''', (user['name'], generate_password_hash(user['password']), id))
        mysql.connection.commit()
        cur.execute('''SELECT * FROM users WHERE id = %s''', (id,))
        rv = cur.fetchone()
        field_names = [i[0] for i in cur.description]
        cur.close()
        result = dict(zip(field_names, rv))
        return jsonify (result) , 201
        # return {'status': 'success'}

    @app.route('/user/<id>', methods=['DELETE'])
    @token_required
    def delete(current_user,id):
        cur = mysql.connection.cursor()
        cur.execute('''DELETE FROM users WHERE id = %s''', (id,))
        mysql.connection.commit()
        cur.close()
        return {'status': 'success'}
    

@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users WHERE username = %s ''', (auth.username,)) 
    rv = cur.fetchone()
    
    field_names = [i[0] for i in cur.description]
    if len(rv) == 0:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    pass_index = field_names.index('password')
    pid_index = field_names.index('id')

    if check_password_hash(rv[pass_index], auth.password):
        my_date = datetime.datetime.now(pytz.timezone('Asia/Dhaka'))
        print(my_date)
        token = jwt.encode({'id': rv[pid_index], 'exp': my_date + datetime.timedelta(hours=3)}, app.config['SECRET_KEY'] ,algorithm="HS256")
        cur.execute('''UPDATE users SET jwt_token = %s, last_login = %s WHERE id = %s''', (token, my_date , rv[pid_index]))
        return jsonify({'token': token})
    
    cur.close()
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
