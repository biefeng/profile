# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/07 14:17
# file_name : rest.py.py
from flask import request

from . import enums
from jsonpickle import pickler

import sys


@enums.route("/<string:name>")
def get_enum_name_and_val(name):
    module_ = sys.modules['app.enums']
    cls = getattr(module_, name)
    values = list(cls)
    result = []
    for v in values:
        result.append({'name': v.name, 'value': v.value})
    return pickler.encode(result)


@enums.route("/", methods=['POST'])
def get_enums_name_and_val():
    module_ = sys.modules['app.enums']
    request_data = request.json
    result = {}
    if request_data is None or not isinstance(request_data, list):
        return {}
    for item in request_data:
        if not isinstance(item, str):
            continue
        cls = getattr(module_, item)
        values = list(cls)
        tmp = []
        for v in values:
            tmp.append({'name': v.name, 'value': v.value})
        result[item] = tmp
    return pickler.encode(result)
