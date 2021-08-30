
from models import response
from app import app ,mysql
import pytz
from flask import make_response ,request, jsonify
from werkzeug.security import check_password_hash
from services.user_service import User_service
import datetime
import jwt

@app.route('/login')
def login():
    auth = request.authorization
    print(auth)
    response = User_service.user_login(auth)
    return jsonify(response)
    # if not auth or not auth.username or not auth.password:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    # cur = mysql.connection.cursor()
    # cur.execute('''SELECT * FROM users WHERE username = %s ''', (auth.username,)) 
    # rv = cur.fetchone()
    
    # field_names = [i[0] for i in cur.description]
    # if len(rv) == 0:
    #     return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    
    # pass_index = field_names.index('password')
    # pid_index = field_names.index('id')

    # if check_password_hash(rv[pass_index], auth.password):
    #     my_date = datetime.datetime.now(pytz.timezone('Asia/Dhaka'))
    #     print(my_date)
    #     token = jwt.encode({'id': rv[pid_index], 'exp': my_date + datetime.timedelta(hours=3)}, app.config['SECRET_KEY'] ,algorithm="HS256")
    #     cur.execute('''UPDATE users SET jwt_token = %s, last_login = %s WHERE id = %s''', (token, my_date , rv[pid_index]))
    #     return jsonify({'token': token})
    
    # cur.close()
    # return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})