# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request
from flask_login import login_required, current_user
from jsonpickle import pickler
from app.enums import ARTICLE_TYPE, DISPLAY_TYPE
import html

from jsonpickle import pickler
from app import db
from app.models import Article
from . import article

import json


@article.route("/list-data", methods=['GET'])
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
        if not current_user.is_authenticated and item.private == DISPLAY_TYPE.私密.value:
            continue
        art_dict = item.to_dict(['content', 'content_md'])
        art_dict['source'] = item.source.name
        articles.append(art_dict)
    result = {
        'total': paginate.total,
        'list': articles
    }

    return Response(pickler.encode(result), status=200, mimetype="application/json")


@login_required
@article.route("/del", methods=["POST"])
def del_article():
    request_data = request.json
    if request_data is None or request_data['ids'] is None:
        return {}
    for ai in request_data['ids']:
        article = Article.query.get_or_404(ai)
        db.session.delete(article)
    return {}


@login_required
@article.route("/save", methods=["POST"])
def save_article():
    request_data = request.json
    if request_data is None:
        return
    id_ = request_data['id']
    if id_:
        Article.query.filter_by(id=id_).update(request_data)
    else:
        art = Article(title=request_data['title'], content=html.escape(request_data['content']), summary=request_data['summary'], source_id=ARTICLE_TYPE.原创.value, articleType_id=1, content_md=request_data['content_md'])
        db.session.add(art)
    db.session.commit()
    return {}


@article.route("/get", methods=["GET"])
def get_article():
    ai = request.args.get("id")
    if ai is not None:
        art = Article.query.get_or_404(ai)
        art.content = html.unescape(art.content)
        if current_user.is_authenticated:
            return art.to_dict()
        else:
            return {"content": art.content}
