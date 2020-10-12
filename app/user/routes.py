# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/05 10:14
# file_name : routes.py
from flask import redirect, url_for, render_template
from flask_login import login_required, logout_user

from . import user


@user.route('/login_view', methods=['GET', 'POST'])
def login_view():
    return render_template('base/login.html')


@user.route('/logout-view')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('admin.home'))
