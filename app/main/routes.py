# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 19:49
# file_name : routes.py

from flask import render_template

from . import main

from config.menu import get_menu


@main.route('/')
def index_new():
    return render_template('base/index.html', component='article/article_list.vue')


@main.route('/test')
def test():
    print(get_menu())
    return render_template('base/index.html', component='test.vue', menu=get_menu(mode='horizontal'))
