# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/01 13:38
# file_name : rest.py
from flask import request, current_app, render_template, Response
from jsonpickle import pickler

from app.models import ChromePlugin
from . import chrome_plugin


@chrome_plugin.route("/list-data", methods=['GET'])
def chrome_plugin_list():
    page_size = request.args.get('pageSize', default=current_app.config['PLUGINS_PER_PAGE'])
    page_number = request.args.get('pageNumber', 0)
    paginate = ChromePlugin.query.order_by().paginate(int(page_number), per_page=int(page_size), error_out=True)
    items = paginate.items
    result = {
        'total': paginate.total,
        'list': items
    }
    return Response(pickler.encode(result), status=200, mimetype="application/json")


@chrome_plugin.route("/detail-data/<int:id>", methods=['GET'])
def chrome_plugin_detail(id):
    plugin = ChromePlugin.query.get_or_404(id)
    return Response(pickler.encode(plugin), status=200, mimetype="application/json")
