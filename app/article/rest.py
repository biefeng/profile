# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request
from flask_login import login_required
from jsonpickle import pickler
from app.enums import ARTICLE_TYPE
import html

from jsonpickle import pickler
from app import db
from app.models import Article
from . import article


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
        article = {'id': item.id, 'summary': item.summary, 'title': item.title, 'create_time': str(item.create_time), 'num_of_view': item.num_of_view, 'sourceStr': item.source.name, 'source': item.source.id}
        articles.append(article)
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

    if request_data:
        request_data['content'] = html.escape(request_data['content'])
        art = Article(title=request_data['title'], content=html.escape(request_data['content']), source_id=ARTICLE_TYPE.原创.value, articleType_id=1, content_md=request_data['contentMd'])
        db.session.add(art)
        db.session.commit()
    print(art)
    return {}


@article.route("/get", methods=["GET"])
@login_required
def get_article():
    ai = request.args.get("id")
    if ai is not None:
        art = Article.query.get_or_404(ai)
        art.content = html.unescape(art.content)
    return pickler.encode(art)
