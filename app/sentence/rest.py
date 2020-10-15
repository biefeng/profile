# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request, jsonify
from flask_jwt import jwt_required
from app.models import Sentence
from app.shard import db, BusinessException
from app.sentence import sentence
from random import random


@sentence.route("/random_get", methods=['GET'])
def random_get():
    _id = request.args.get("id")
    _query = Sentence.query
    _count = _query.count()

    _sentence = _query.filter(Sentence.id != _id).offset(int(random() * (_count - 1))).limit(1).first()
    if _sentence is not None:
        return _sentence.to_dict()
    return {}
