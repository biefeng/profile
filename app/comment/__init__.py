# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:05
# file_name : __init__.py.py

from flask import Blueprint

comment = Blueprint('comment', __name__)

from . import rest, routes
