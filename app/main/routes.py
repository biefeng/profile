# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 19:49
# file_name : routes.py

from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, make_response, current_app
from jsonpickle import pickler

from app.shard import cache
from config.menu import get_menu
from . import main


@main.route('/')
@cache.cached(timeout=50)
def index_new():
    return redirect(url_for("article.article_list_view"))


@main.route('/xml', methods=['GET'])
def sitemap_xml():
    try:
        """Generate sitemap.xml. Makes a list of urls and date modified."""
        pages = []
        ten_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
        # static pages
        for rule in current_app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments) == 0:
                pages.append(
                    ["http://pythonprogramming.net" + str(rule.rule), ten_days_ago]
                )
        # sitemap_xml = render_template('sitemap_template.xml', pages=pages)
        response = make_response(pickler.encode(pages))
        response.headers["Content-Type"] = "application/xml"

        return response
    except Exception as e:
        return (str(e))


@main.route("/site.txt", methods=['GET'])
def sitemap_txt():
    raise Exception('ni')
    return current_app.send_static_file("site.txt")


@main.route('/test')
def test():
    print(get_menu())
    return render_template('base/index.html', component='test.vue', menu=get_menu(mode='horizontal'))


@main.route("/baidu_verify_xii8wDagbI.html")
def ddddddddd():
    return render_template("baidu_verify_xii8wDagbI.html")
