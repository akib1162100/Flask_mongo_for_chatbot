# -*- coding: utf-8 -*-
import locale
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from flask_mysqldb import MySQL


locale.setlocale(locale.LC_TIME, locale.getlocale())

app = Flask(__name__)
app.config.from_object('config')

mysql = MySQL(app)