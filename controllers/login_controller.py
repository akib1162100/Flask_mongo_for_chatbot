
from app import app 
from flask import request
from services.user_service import User_service

@app.route('/login')
def login():
    auth = request.authorization
    response = User_service.user_login(auth)
    return response