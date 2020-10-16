# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request, jsonify
from flask_jwt import jwt_required
from app.models import Sentence, Article
from app.shard import db, BusinessException
from app.sentence import sentence
from random import random
import jsonpickle


@sentence.route("/random_get", methods=['GET'])
def random_get():
    _id = request.args.get("id")
    _query = Sentence.query
    _count = _query.count()
    _sentence = _query.filter(Sentence.id != _id).offset(int(random() * (_count - 1))).limit(1).first()
    if _sentence is not None:
        return _sentence.to_dict()
    return {}


@sentence.route("/list", methods=['GET'])
def list_data():
    _page_size = request.args.get("pageSize", 10)
    _page_number = request.args.get("pageNumber", 1)
    _paginate = Sentence.query.paginate(int(_page_number), per_page=int(_page_size), error_out=True)
    _result = {
        'total': _paginate.total,
        'list': [i.to_dict() for i in _paginate.items]
    }
    return jsonpickle.encode(_result, unpicklable=False, keys=True)


@sentence.route("/save", methods=['POST'])
def save_data():
    _json_data = request.json
    _s = Sentence(content=_json_data.get("content"), author=_json_data.get("author"),
                  original_source=_json_data.get("original_source"))
    db.session.add(_s)
    db.session.commit()
    return {}, 200


@sentence.route("/delete", methods=['DELETE'])
def delete_data():
    _id = request.args.get("id")
    if _id is None:
        return {}
    Sentence.query.filter(Sentence.id == _id).delete()
    db.session.commit()
    return {}, 200
