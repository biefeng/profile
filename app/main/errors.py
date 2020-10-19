from flask import render_template
from flask_cors import cross_origin

from . import main
from .. import BusinessException


@main.app_errorhandler(403)
def forbidden(e):
    return "无权限", 403


@main.app_errorhandler(404)
@cross_origin(supports_credentials=True)
def page_not_found(e):
    return "请求地址错误", 404


@main.app_errorhandler(BusinessException)
def business_exception(_err):
    return {
               "status": "-1",
               "message": _err.err_msg
           }, 500

# @main.app_errorhandler(500)
# def internal_server_error(e):
#     return render_template('base/index.html', component="base/500.vue"), 500
