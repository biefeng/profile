# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : routes.py
from flask import render_template
from flask_login import login_required
from . import article


@article.route("/edit", methods=["GET"])
@login_required
def create_article():
    return render_template('base/admin.html', component='article/article_editor.vue')


@article.route("/edit/<int:id>", methods=["GET"])
@login_required
def edit_article(id):
    return render_template('base/admin.html', id=id, component='article/article_editor.vue')
