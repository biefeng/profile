# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/05 10:14
# file_name : rest.py


from flask import request
from flask_login import login_user

from app.models import User
from . import auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    request_data = request.json
    username_ = request_data['username']
    password_ = request_data['password']
    result = {}
    if username_ is not None:
        lu = User.query.filter_by(username=username_).first()
        if lu is not None and lu.verify_password(password_):
            login_user(lu)
            result['msg'] = "login successfully"
            result['status'] = 1
        else:
            result['err_msg'] = "username or password error"
            result['status'] = 0
    return result
