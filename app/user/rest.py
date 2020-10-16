# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/05 10:14
# file_name : rest.py


from flask import request
from flask_jwt import jwt_required
from app.models import User
import requests
from . import user
import time


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


@user.route('/github/access/token', methods=['POST'])
def github_access_token():
    json_data = request.json
    _code = json_data.get("code")
    _state = json_data.get("state")

    if _code is not None:
        limit = 4
        for o in limit:
            try:
                res = requests.post("https://github.com/login/oauth/access_token",
                                    headers={"Accept": "application/json"},
                                    data={"code": _code, "state": _state, "client_id": "b1fab3539af78d4ad4b5",
                                          "client_secret": "71dcffc193caab6d12d986dd9d78515c744d32fd"})

                res_json = res.json()
                _access_token = res_json.get("access_token")
            except requests.exceptions.ConnectionErrora as e:
                if o < (limit - 1):
                    time.sleep(0.5)

            else:
                time.sleep(0.1)
                break

        for o in limit:
            try:
                if _access_token is not None:
                    res = requests.get("https://api.github.com/user",
                                       headers={"Authorization": "token " + _access_token,
                                                "Accept": "application/vnd.github.v3+json",
                                                'Connection': 'close'}, verify=False)
                    return res.json()
            except requests.exceptions.ConnectionErrora as e:
                if o < (limit - 1):
                    time.sleep(0.5)

            else:
                time.sleep(0.1)
                break
