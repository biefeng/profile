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
@admin.route("/list-articles", methods=['GET'])
def article_list():
    page_size = request.args.get('pageSize', 10)
    page_number = request.args.get('pageNumber', 0)
    query = Article.query
    source = request.args.get("source")

    if source is not None:
        query = query.filter(Article.source_id == source)
    category = request.args.get("category")
    if category is not None:
        query = query.filter(Article.articleType_id == category)
    paginate = query.order_by(Article.create_time.desc()).paginate(int(page_number), per_page=int(page_size), error_out=True)
    items = paginate.items
    articles = []
    for item in items:
        article = {'id': item.id, 'title': item.title, 'create_time': str(item.create_time), 'num_of_view': item.num_of_view, 'source': item.source.name}
        articles.append(article)
    result = {
        'total': paginate.total,
        'list': articles
    }
    return Response(pickler.encode(result), status=200, mimetype="application/json")


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


@login_required
@admin.route("/list-chrome-plugins", methods=['GET'])
def chrome_plugin_list():
    page_size = request.args.get('pageSize', 10)
    page_number = request.args.get('pageNumber', 0)
    paginate = ChromePlugin.query.order_by(ChromePlugin.create_time.desc()).paginate(int(page_number), per_page=int(page_size), error_out=True)
    items = paginate.items
    result = {
        'total': paginate.total,
        'list': items
    }
    return Response(pickler.encode(result), status=200, mimetype="application/json")
