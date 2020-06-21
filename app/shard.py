# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/10 19:21
# file_name : shard.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy()
