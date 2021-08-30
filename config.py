# -*- coding: utf-8 -*-
import os
import yaml

basedir = os.path.abspath(os.path.dirname(__file__))

db = yaml.load(open('db_credential.yml'))

SECRET_KEY = 'soft@2019'
MYSQL_HOST = db['mysql_host']
MYSQL_USER = db['mysql_user']
MYSQL_PASSWORD= db['mysql_password']
MYSQL_DB= db['mysql_database']