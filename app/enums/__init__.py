# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/30 19:20
# file_name : __init__.py.py
from enum import Enum

from flask import Blueprint

enums = Blueprint('enum', __name__)

from . import rest


class ARTICLE_TYPE(Enum):
    原创 = 1
    翻译 = 2
    转载 = 3

    @staticmethod
    def get_name_by_val(value):
        values = list(ARTICLE_TYPE)
        for val in values:
            if value == val.value:
                return val.name


class DISPLAY_TYPE(Enum):
    私密 = 0
    公开 = 1


class CHROME_PLUGIN_CATEGORY:
    生产工具 = 0
    开发者工具 = 1


if __name__ == '__main__':
    print(ARTICLE_TYPE.get_name_by_val(1))
