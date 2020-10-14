# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request, jsonify
from flask_jwt import jwt_required
from app.models import Comment
from app.shard import db, BusinessException
from . import comment


@comment.route("/list", methods=['GET'])
def list_comments():
    article_id = request.args.get("article_id")
    _query = Comment.query
    _list = _query.filter(Comment.article_id == article_id).order_by(Comment.timestamp.desc()).all()
    _result = [i.to_dict() for i in _list]
    return jsonify(_result)


@comment.route("/save", methods=['POST'])
def save_comment():
    json_data = request.json
    _comment = Comment(content=json_data['html'], content_md=json_data['html'],
                       article_id=json_data['article_id'])
    db.session.add(_comment)
    db.session.commit()
    return Response()


@comment.route("/delete", methods=['POST'])
@jwt_required()
def delete_comment():
    json_data = request.json
    _com_id = json_data.get("id")
    if _com_id is None:
        raise BusinessException("评论不存在")
    Comment.query.filter(Comment.id == _com_id).delete()
    db.session.commit()
    return Response()
