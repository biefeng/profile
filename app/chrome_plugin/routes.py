# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/01 13:38
# file_name : routes.py


from flask import render_template
from flask_login import login_required

from app.models import ChromePlugin

from . import chrome_plugin


@chrome_plugin.route('/list', methods=['GET'])
def plugin_list():
    return render_template('base/index.html', component='chrome_plugin/plugin_list.vue')


@chrome_plugin.route('/detail/<int:id>', methods=['GET'])
def plugin_detail(id):
    return render_template('base/index.html', id=id, component='chrome_plugin/plugin_detail.vue')


@chrome_plugin.route('/spider', methods=['GET'])
@login_required
def plugin_spider():
    return render_template('base/admin.html', component='chrome_plugin/plugin_spider.vue')
