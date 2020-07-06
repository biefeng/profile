# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/05 10:14
# file_name : rest.py


from flask import request
from flask_login import login_user

from app.models import User
from . import user


@user.route('/login', methods=['GET', 'POST'])
def login():
    pass
