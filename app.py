import locale
from flask import Flask
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import yaml
from flask_pymongo import PyMongo

locale.setlocale(locale.LC_TIME,locale.getlocale())

app = Flask(__name__)
db = yaml.load(open('config.yml'))


SECRET_KEY = 'soft@2019'

app.config['MONGO_URI'] = db['mongo_uri']
mongo = PyMongo(app)
app.config['SECRET_KEY'] = 'soft@2019'

'''for mysql'''
# MYSQL_HOST = db['mysql_host']
# MYSQL_USER = db['mysql_user']
# MYSQL_PASSWORD= db['mysql_password']
# MYSQL_DB= db['mysql_database']
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['MYSQL_HOST']= db['mysql_host']
# app.config['MYSQL_USER']= db['mysql_user']
# app.config['MYSQL_PASSWORD']= db['mysql_password']
# app.config['MYSQL_DB']= db['mysql_database']

mysql = MySQL(app)
database = SQLAlchemy(app)

'''for mysql'''

import models
import controllers
import services
import repository