# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/29 21:11
# file_name : rest.py

from flask import Response, request
from flask_login import login_required
from jsonpickle import pickler

from app.models import Article, ChromePlugin
from . import admin
from app.shard import db


@admin.route("/get_json", methods=["POST"])
def get_json():
    map = {}
    map['name'] = "biefeng"
    return map


@login_required
@admin.route("/del-article", methods=["POST"])
def del_article():
    request_data = request.json
    if request_data is None or request_data['ids'] is None:
        return {}
    for ai in request_data['ids']:
        article = Article.query.get_or_404(ai)
        db.session.delete(article)
    return {}
