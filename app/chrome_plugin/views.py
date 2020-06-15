# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/14 3:19
# file_name : views.py.py

from flask import request, current_app, render_template

from app.models import ChromePlugin
from . import chrome_plugin


@chrome_plugin.route('/list', methods=['GET', 'POST'])
def plugin_list():
    page = request.args.get('page', 1, type=int)
    pagination = ChromePlugin.query.order_by(ChromePlugin.create_time.desc()).paginate(
        page, per_page=current_app.config['PLUGINS_PER_PAGE']
    )
    plugins = pagination.items
    return render_template('chrome_plugin/plugin_list.html', pagination=pagination, plugins=plugins, endpoint='.plugin_list')


@chrome_plugin.route('/detail/<int:id>', methods=['GET', 'POST'])
def plugin_detail(id):
    plugin = ChromePlugin.query.get_or_404(id)
    return render_template('chrome_plugin/plugin_detail.html', plugin=plugin)
