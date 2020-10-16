# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py
import jsonpickle
from flask import Response, request, jsonify
from flask_jwt import jwt_required

from app.models import Comment, Article
from app.shard import db, BusinessException
from . import comment


@comment.route("/list", methods=['GET'])
def list_comments():
    article_id = request.args.get("article_id")
    if article_id is None:
        raise BusinessException("未找到该文章")
    _query = Comment.query
    _list = _query.filter(Comment.article_id == article_id).order_by(Comment.timestamp.desc()).all()
    _result = [i.to_dict() for i in _list]
    return jsonify(_result)


@comment.route("/admin/list", methods=['GET'])
@jwt_required()
def admin_list_comments():
    _page_number = request.args.get("pageNumber", 1)
    _page_size = request.args.get("pageSize", 10)
    _paginate = Comment.query.paginate(int(_page_number), per_page=int(_page_size), error_out=True)
    _item = _paginate.items
    _comments = []
    for _comment in _item:
        _comment_to_dict = _comment.to_dict()
        _article_id = _comment.article_id
        if _article_id is not None:
            _article = Article.query.filter(Article.id == _article_id).first()
            if _article is not None:
                _comment_to_dict['title'] = _article['title']
        _comments.append(_comment_to_dict)
    _result = {
        'total': _paginate.total,
        'list': _comments
    }
    return jsonpickle.encode(_result, unpicklable=False, keys=True)


@comment.route("/save", methods=['POST'])
def save_comment():
    json_data = request.json
    _comment = Comment(content=json_data['content'], content_md=json_data['content_md'],
                       article_id=json_data['article_id'], avatar_hash=json_data.get("avatar_hash"),
                       author_name=json_data.get("author_name"))
    db.session.add(_comment)
    db.session.commit()
    return Response()


@comment.route("/delete", methods=['DELETE'])
@jwt_required()
def delete_comment():
    _com_id = request.args.get("id")
    if _com_id is None:
        raise BusinessException("评论不存在")
    Comment.query.filter(Comment.id == _com_id).delete()
    db.session.commit()
    return Response()
