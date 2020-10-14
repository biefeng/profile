import logging

from flask import Flask, before_render_template, request
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_jwt import JWT, _jwt
from jwt import InvalidTokenError
from werkzeug.security import safe_str_cmp

from app.models import ArticleType, article_types, Source, \
    Comment, Article, Menu, BlogInfo, \
    Plugin, BlogView, User
from app.shard import db, login_manager, cache, cache_config, BusinessException
from config.config import Config

LOGGER = logging.getLogger(__name__)

bootstrap = Bootstrap()
moment = Moment()


def create_app():
    app = Flask(__name__)
    log_slow_query(app)
    enable_cache(app)
    app.config.from_object(Config)
    Config.init_app(app)
    # CSRFProtect(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    registry_routes(app)
    CORS(app, supports_credentials=True)
    Migrate(app, db)
    jwt = init_jwt(app)
    before_request(app)
    register_error_handle(app)
    return app


def init_jwt(app):
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            return user

    def identify(payload):
        identify_ = payload['identity']
        return User.query.filter_by(id=identify_).first()

    return JWT(app, authenticate, identify)


def before_request(app):
    def f1():
        pass

    app.before_request(f1)


def register_error_handle(app):
    def err_handle_func(_err):
        return {
                   "status": "-1",
                   "message": _err.err_msg
               }, 500

    app.register_error_handler(BusinessException, err_handle_func)


def registry_routes(app):
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .enums import enums as enum_blueprint
    app.register_blueprint(enum_blueprint, url_prefix='/enum')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .chrome_plugin import chrome_plugin as chrome_plugin_blueprint
    app.register_blueprint(chrome_plugin_blueprint, url_prefix='/chrome-plugin')

    from .comment import comment as comment__blueprint
    app.register_blueprint(comment__blueprint, url_prefix='/comment')

    from .article import article as article_blueprint
    app.register_blueprint(article_blueprint, url_prefix='/article')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')


def log_slow_query(app):
    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            if query.duration >= app.config['FLASKY_DB_QUERY_TIMEOUT']:
                LOGGER.debug('#####Slow query:%s \nParameters:%s \nDuration:%fs\nContext:%s\n #####' %
                             (query.statement % query.parameters, query.parameters, query.duration,
                              query.context))  # 打印超时sql执行信息
        return response

    @app.teardown_request
    def handle_teardown_request(ex):
        pass


def template_context_handle_before_render(app):
    @before_render_template.connect_via(app)
    def before_render_template_signal(sender, template, context, **extra):
        if 'component' in context:
            print("+++++++++++++++++++++++++++++++++++")
        else:
            context['component'] = "sample.vue"
            print("===================================")

        # template_globals = template.globals
        # params = {}
        # for k, v in context.items():
        #     if k not in template_globals:
        #         params[k] = v
        # context['context'] = pickler.encode(params)
        # context['context'] = {}


def enable_cache(app):
    cache.init_app(app, cache_config)
