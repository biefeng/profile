# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/05 10:14
# file_name : rest.py


from flask import flash, redirect, url_for, render_template, request, Response
from flask_login import login_required, logout_user, login_user

from . import auth
from .forms import LoginForm
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if user is not None and user.verify_password(form.password.data):
    #         login_user(user)
    #         flash(u'登陆成功！欢迎回来，%s!' % user.username, 'success')
    #         return redirect(request.args.get('next') or url_for('main.index'))
    #     else:
    #         flash(u'登陆失败！用户名或密码错误，请重新登陆。', 'danger')
    # if form.errors:
    #     flash(u'登陆失败，请尝试重新登陆.', 'danger')
    request_data = request.json
    email_ = request_data['email']
    password_ = request_data['password']
    result = {}
    if email_ is not None:
        lu = User.query.filter_by(email=email_).first()
        if lu is not None and lu.verify_password(password_):
            login_user(lu)
            result['msg'] = "login successfully"
        else:
            result['err_msg'] = "username or password error"
            return Response(response=result, status=403, mimetype="application/json")
    return result
