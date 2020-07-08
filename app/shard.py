# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/10 19:21
# file_name : shard.py

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
from functools import wraps
from config.config import Config

from flask_caching import Cache

from functools import wraps
from flask import request

logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.dialects').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
# logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login_view'

db = SQLAlchemy()

LOGGER = logging.getLogger(__name__)


def handle_template_render_exception(func):
	@wraps(func)
	def decorated_view(*args, **kwargs):
		rendered_template = func(*args, **kwargs)
		return rendered_template

	return decorated_view


def cache_request_data(func):
	"""
	缓存装饰器
	:param func:
	:return:
	"""

	@wraps(func)
	def decorated_view(*args, **kwargs):
		data = request.get_data()
		request_args = request.args

		cache_key = request.url
		if data is not None:
			cache_key += ("-" + str(data, encoding="utf-8"))
			cache_key += ("-" + str(request_args))
			cached_data = cache.get(cache_key)
			if cached_data is not None:
				LOGGER.debug("the data return from cache")
				return cached_data
		rendered_template = func(*args, **kwargs)
		cache.set(cache_key, rendered_template)
		return rendered_template

	return decorated_view


cache = Cache()

cache_config = {
	"DEBUG": True,  # some Flask specific configs
	"CACHE_TYPE": "simple",  # Flask-Caching related configs
	"CACHE_DEFAULT_TIMEOUT": 3600
}
