# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request
from jsonpickle import pickler

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
        article = {'id': item.id, 'summary': item.summary, 'title': item.title, 'create_time': str(item.create_time), 'num_of_view': item.num_of_view, 'source': item.source.name}
        articles.append(article)
    result = {
        'total': paginate.total,
        'list': articles
    }
    return Response(pickler.encode(result), status=200, mimetype="application/json")
