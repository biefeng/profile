from flask import render_template

from . import main


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('base/index.html', component="base/403.vue"), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('base/index.html', component="base/404.vue"), 404


# @main.app_errorhandler(500)
# def internal_server_error(e):
#     return render_template('base/index.html', component="base/500.vue"), 500
