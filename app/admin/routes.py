# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/30 16:31
# file_name : routes.py
from flask import render_template, redirect, url_for
from flask_login import login_required

from . import admin


@admin.route('/')
@login_required
def home():
    return redirect(url_for('admin.manage_articles'))


@admin.route('/edit-article')
@login_required
def edit_article():
    return render_template('base/admin.html', component="article/article_editor.vue")


@admin.route('/index')
@login_required
def index():
    return render_template('base/index.html', component="admin/article-list.vue")


@admin.route('/manage-articles', methods=['GET', 'POST'])
@login_required
def manage_articles():
    return render_template('base/admin.html', component="admin/article-list.vue")


@admin.route('/manage-plugins', methods=['GET', 'POST'])
@login_required
def manage_plugins():
    return render_template('base/admin.html', component="admin/chrome-plugin-list.vue")
