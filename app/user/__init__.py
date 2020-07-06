# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/06 12:58
# file_name : __init__.py.py

from flask import Blueprint

user = Blueprint('user', __name__)

from . import routes, rest
