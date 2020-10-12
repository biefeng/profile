# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/05 10:14
# file_name : rest.py


from flask import request
from flask_jwt import jwt_required
from app.models import User
from . import user


def gravatar(h, size=40):
    _avatar_url = 'https://gravatar.loli.net/avatar'
    return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
        url=_avatar_url, hash=h, size=size, default="identicon", rating="g")


@user.route('/info', methods=['GET'])
@jwt_required()
def info():
    _username = request.args.get("u")
    if _username is None:
        return ""
    _user_info = User.query.filter_by(username=_username).first()
    if _user_info is not None:
        _user_info = _user_info.to_dict()
        return {
            "username": _user_info.get("username"),
            "avatar": gravatar(_user_info.get("avatar_hash"))
        }
    return ""
