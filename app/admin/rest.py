# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/29 21:11
# file_name : rest.py

from flask import Response, request
from flask_login import login_required
from jsonpickle import pickler

from app.models import Article, ChromePlugin, User
from . import admin
from app.shard import db


@admin.route("/get_json", methods=["POST"])
@login_required
def get_json():
    map = {}
    map['name'] = "biefeng"
    return map


@admin.route("/user/list", methods=["GET"])
@login_required
def list_users():
    query_list = User.query.all()
    user_list = []
    for i in query_list:
        user_list.append({'email': i.email, 'username': i.username, 'avatar_hash': i.avatar_hash})
    return pickler.encode({'list': query_list, 'total': 1})


@admin.route("/user/add", methods=["POST"])
@login_required
def add_user():
    request_data = request.json
    email_ = request_data['email']
    username_ = request_data['username']
    password_ = request_data['password']
    user = User(username=username_, password=password_, email=email_)
    db.session.add(user)
    db.session.commit()
    return {}


@admin.route("/user/del", methods=["POST"])
@login_required
def delete_user():
    request_data = request.json
    username_ = request_data['username']
    if username_ == 'admin':
        return {'msg': "admin can't be deleted"}
    user = User.query.filter_by(username=username_).first()
    db.session.delete(user)
    db.session.commit()
