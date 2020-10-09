# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

import html, json

from flask import Response, request
from flask_jwt import jwt_required
from jsonpickle import pickler

from app import db
from app.enums import ARTICLE_TYPE, DISPLAY_TYPE, ARTICLE_TAGS
from app.models import Article
from app.shard import authenticated_user
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

    paginate = query.paginate(int(page_number), per_page=int(page_size), error_out=True)
    items = paginate.items
    articles = []
    for item in items:
        if not authenticated_user.is_auth() and item.private == DISPLAY_TYPE.私密.value:
            continue
        art_dict = item.to_dict(['content', 'content_md'])
        art_dict['source'] = item.source.name
        if item.tags is not None:
            _tags = json.loads(item.tags)
            art_dict['tags'] = ARTICLE_TAGS.get_names_by_values(_tags)
        else:
            art_dict['tags'] = []

        articles.append(art_dict)
    result = {
        'total': paginate.total,
        'list': articles
    }

    return Response(pickler.encode(result), status=200, mimetype="application/json")


@article.route("/del", methods=["POST"])
@jwt_required()
def del_article():
    request_data = request.json
    if request_data is None or request_data['ids'] is None:
        return {}
    for ai in request_data['ids']:
        _article = Article.query.get(ai)
        if _article is not None:
            db.session.delete(_article)
    return {}


@article.route("/save", methods=["POST"])
@jwt_required()
def save_article():
    request_data = request.get_json()
    if request_data is None:
        return
    id_ = request_data.get('id')
    request_data['tags'] = json.dumps(request_data.get("tags"))
    if id_:
        Article.query.filter_by(id=id_).update(request_data)
    else:
        art = Article(title=request_data.get('title'), content=html.escape(request_data.get('content')),
                      summary=request_data.get('summary'), source_id=ARTICLE_TYPE.原创.value, articleType_id=1,
                      content_md=request_data.get('content_md'), tags=request_data.get("tags"))
        db.session.add(art)
    db.session.commit()
    return {}


@article.route("/get", methods=["GET"])
def get_article():
    ai = request.args.get("id")
    if ai is not None:
        art = Article.query.get_or_404(ai)
        art.content = html.unescape(art.content)

        return art.to_dict()
