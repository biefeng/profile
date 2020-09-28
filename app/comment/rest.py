# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request, jsonify

from app.models import Comment
from app.shard import db
from . import comment


@comment.route("/list", methods=['GET'])
def list_comments():
    article_id = request.args.get("article_id")
    _query = Comment.query
    _list = _query.filter(Comment.article_id == article_id).all()
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
