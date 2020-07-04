from flask import Flask, before_render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFProtect

from app.models import ArticleType, article_types, Source, \
    Comment, Article, Menu, BlogInfo, \
    Plugin, BlogView
from app.shard import db, login_manager

from config.config import Config

bootstrap = Bootstrap()
moment = Moment()


def create_app():
    app = Flask(__name__)

    log_slow_query(app)

    template_context_signal(app)

    app.config.from_object(Config)
    Config.init_app(app)
    CSRFProtect(app)

    db.init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    init_jinja_ctx(app)
    registry_routes(app)
    Migrate(app, db)
    return app


def init_jinja_ctx(app):
    """
        Global variables to jiajia2 environment:
        :arg app
    """
    app.jinja_env.globals['ArticleType'] = ArticleType
    app.jinja_env.globals['article_types'] = article_types
    app.jinja_env.globals['Menu'] = Menu
    app.jinja_env.globals['BlogInfo'] = BlogInfo
    app.jinja_env.globals['Plugin'] = Plugin
    app.jinja_env.globals['Source'] = Source
    app.jinja_env.globals['Article'] = Article
    app.jinja_env.globals['Comment'] = Comment
    app.jinja_env.globals['BlogView'] = BlogView


def registry_routes(app):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .chrome_plugin import chrome_plugin as chrome_plugin_blueprint
    app.register_blueprint(chrome_plugin_blueprint, url_prefix='/chrome-plugin')

    from comment import comment as comment__blueprint
    app.register_blueprint(comment__blueprint, url_prefix='/comment')

    from .article import article as article_blueprint
    app.register_blueprint(article_blueprint, url_prefix='/article')


def log_slow_query(app):
    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            if query.duration >= app.config['FLASKY_DB_QUERY_TIMEOUT']:
                print('#####Slow query:%s \nParameters:%s \nDuration:%fs\nContext:%s\n #####' %
                      (query.statement, query.parameters, query.duration, query.context))  # 打印超时sql执行信息
        return response


def template_context_signal(app):
    @app.teardown_request
    def handle_teardown_request(ex):
        pass

    @before_render_template.connect_via(app)
    def log_template_renders(sender, template, context, **extra):
        template_globals = template.globals
        params = {}
        for k, v in context.items():
            if k not in template_globals:
                params[k] = v
        # context['context'] = pickler.encode(params)
        context['context'] = {}
