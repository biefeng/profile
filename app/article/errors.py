from flask import render_template

from app.shard import handle_template_render_exception
from . import article


@article.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@article.app_errorhandler(404)
@handle_template_render_exception
def page_not_found(e):
    return render_template('base/admin.html', component="base/404.vue"), 404


@article.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
