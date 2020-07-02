# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 19:49
# file_name : routes.py

from html.parser import HTMLParser

from flask import render_template, request, current_app, redirect, \
    url_for, flash

from . import main
from .forms import CommentForm
from .. import db
from ..models import Article, ArticleType, Comment, \
    Follow, User, Source, BlogView, ChromePlugin


@main.route('/new')
def index_new():
    return render_template('base/index.html', component='article/article_list.vue')
