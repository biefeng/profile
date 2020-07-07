# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/07 10:17
# file_name : rest.py

from flask import request, current_app, render_template, Response
from jsonpickle import pickler
from flask import jsonify
from app.models import ArticleType
from . import main


@main.route("/article_type/list", methods=['GET'])
def article_type_list():
    records = ArticleType.query.all()
    result = []
    for record in records:
        record_to_dict = record.to_dict()
        result.append(record_to_dict)
    return jsonify(result)
