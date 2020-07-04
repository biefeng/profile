# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/02 23:06
# file_name : rest.py

from flask import Response, request
from flask_login import login_required
from jsonpickle import pickler
from app.enums import ARTICLE_TYPE
import html

from jsonpickle import pickler
from app import db
from app.models import Article
from . import comment


@comment.route("/list-data", methods=['GET'])
def list_comments():
    pass
