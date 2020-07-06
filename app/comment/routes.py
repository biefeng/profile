# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : routes.py

from flask import render_template
from flask_login import login_required

from app.shard import handle_template_render_exception
from . import comment


@comment.route("/list-view", methods=["GET"])
@login_required
@handle_template_render_exception
def list_view():
    return render_template('base/admin.html', component='comment/comment_list.vue')
