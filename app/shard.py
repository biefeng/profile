# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/10 19:21
# file_name : shard.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from functools import wraps

logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.dialects').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

db = SQLAlchemy()
