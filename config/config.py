import os
from logging.config import dictConfig

import yaml

basedir = os.path.abspath(os.path.dirname(__file__))

logging_config_file = os.path.join(os.path.dirname(__file__), 'logging.yaml')

#  设置日志
with open(logging_config_file, 'r') as f:
    config = yaml.safe_load(f.read())
    dictConfig(config)


class Config():
    # DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Biefeng123!@106.13.83.252/blog_mini?charset=utf8mb4"
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    PLUGINS_PER_PAGE = 16
    SECRET_KEY = 'secret key to protect from csrf'
    WTF_CSRF_SECRET_KEY = 'random key for form'  # for csrf protection

    FLASKY_DB_QUERY_TIMEOUT = 1
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_ECHO = True

    SQLALCHEMY_ENGINE_OPTIONS = {
        "charset": "utf8mb4"
    }

    # Take good care of 'SECRET_KEY' and 'WTF_CSRF_SECRET_KEY', if you use the
    # bootstrap extension to create a form, it is Ok to use 'SECRET_KEY',
    # but when you use tha style like '{{ form.name.labey }}:{{ form.name() }}',
    # you must do this for yourself to use the wtf, more about this, you can
    # take a reference to the book <<Flask Framework Cookbook>>.
    # But the book only have the version of English.

    @staticmethod
    def init_app(app):
        pass
