from app import app
from flask import jsonify
from flask_restful import Resource ,reqparse
from services.user_service import User_service
from controllers.utils import token_required

class User_controller(Resource):
    global user_parser
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('username', type=str, required=True)
    user_parser.add_argument('password', type=str, required=True)

    
    @app.route('/user')
    @token_required
    def get_all_users(current_user):
        response = User_service.get_all_users()
        return jsonify(response)
    
    @app.route('/user/<user_id>')
    @token_required
    def get_user(current_user,user_id):
        response = User_service.get_user(user_id)
        return jsonify(response)
    
    @app.route('/user/<user_id>', methods=['PUT'])
    @token_required
    def update_user(current_user,user_id):
        user = user_parser.parse_args()
        response= User_service.update_user(user_id,user.username,user.password)
        return jsonify(response)

    @app.route('/user/<user_id>', methods=['DELETE'])
    @token_required
    def delete_user(current_user,user_id):
        response = User_service.delete_user(user_id)
        return jsonify(response)

    @app.route('/user', methods=['POST'])
    @token_required
    def create_user(current_user):
        user = user_parser.parse_args()
        response = User_service.create(user)
        return jsonify(response)
