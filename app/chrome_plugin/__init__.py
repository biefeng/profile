# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/14 3:18
# file_name : __init__.py.py

from flask import Blueprint

chrome_plugin = Blueprint('chrome_plugin', __name__)

from . import routes, rest
