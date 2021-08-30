from typing import Text
from sqlalchemy import Column,String, DateTime, Boolean
from app import database
from models.dbtools import Dictable

class User(object):
    id = database.Column(String(32), primary_key=True)
    username = database.Column(String(255))
    password = database.Column(String(255))
    jwt_token = database.Column(String(255))
    last_login = database.Column(DateTime)
    name_id = database.Column(String(255))
    password_hash = database.Column(String(255))
    team = database.Column(String(255))
    api_token = database.Column(String(4000))
    project = database.Column(String(255))
    username_is_assigned = database.Column(Boolean)
    authentication_mechanism = database.Column(String(255))

    # def __init__(self, id, username, password, jwt_token, last_login, name_id, password_hash, team, api_token, project, username_is_assigned, authentication_mechanism):
    #     self.id = id
    #     self.username = username
    #     self.password = password
    #     self.jwt_token = jwt_token
    #     self.last_login = last_login
    #     self.name_id = name_id
    #     self.password_hash = password_hash
    #     self.team = team
    #     self.api_token = api_token
    #     self.project = project
    #     self.username_is_assigned = username_is_assigned
    #     self.authentication_mechanism = authentication_mechanism

    def user_from_tuples(tuples):
        user = User()
        user.id , user.username, user.password, user.jwt_token, user.last_login, user.name_id, user.password_hash, user.team, user.api_token, user.project, user.username_is_assigned, user.authentication_mechanism = tuples
        return user



    def __repr__(self):
        return self.username