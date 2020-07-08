# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 19:49
# file_name : routes.py

from flask import render_template, redirect, url_for

from . import main

from config.menu import get_menu

from app.shard import cache


@main.route('/')
@cache.cached(timeout=50)
def index_new():
    return redirect(url_for("article.article_list_view"))


@main.route('/test')
def test():
    print(get_menu())
    return render_template('base/index.html', component='test.vue', menu=get_menu(mode='horizontal'))
