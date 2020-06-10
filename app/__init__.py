from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

from app.models import ArticleType, article_types, Source, \
    Comment, Article, User, Menu, ArticleTypeSetting, BlogInfo, \
    Plugin, BlogView
from config import Config
from shard import db, login_manager

bootstrap = Bootstrap()
moment = Moment()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    CSRFProtect(app)

    db.init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    init_jinja_ctx(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
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
