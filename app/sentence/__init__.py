# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:05
# file_name : __init__.py.py

from flask import Blueprint

sentence = Blueprint('sentence', __name__)
from . import rest
