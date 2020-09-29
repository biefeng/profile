# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/07 10:17
# file_name : rest.py
import hashlib

from flask import request, current_app, render_template, Response
from jsonpickle import pickler
from flask import jsonify
from app.models import ArticleType
from . import main
from app.shard import authenticated_user


@main.route("/article_type/list", methods=['GET'])
def article_type_list():
    records = ArticleType.query.all()
    result = []
    for record in records:
        record_to_dict = record.to_dict()
        result.append(record_to_dict)
    return jsonify(result)


@main.route("/checkToken", methods=["POST"])
def check_token():
    if authenticated_user.is_auth():
        return jsonify({"data": 1})
    return jsonify({"data": 0})


@main.route("/avatar", methods=["GET"])
def gravatar(size=40, default='identicon', rating='g'):
    # if request.is_secure:
    #     url = 'https://secure.gravatar.com/avatar'
    # else:
    #     url = 'http://www.gravatar.com/avatar'
    size = request.args.get("size", 18)
    url = 'https://gravatar.loli.net/avatar'
    _hash = hashlib.md5("BieFeNg".encode('utf-8')).hexdigest()
    return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
        url=url, hash=_hash, size=size, default=default, rating=rating)
