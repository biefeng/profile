# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/30 19:20
# file_name : __init__.py.py
from enum import Enum

from flask import Blueprint

enums = Blueprint('enum', __name__)

from app.enums import rest


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


class ARTICLE_TAGS(Enum):
    Git = 0
    Maven = 1
    Java = 2
    Python = 3
    JavaScript = 4
    Vue = 5
    CSS = 6
    HTML = 7
    Spring = 8
    SpringBoot = 9
    Mybatis = 10
    SpringMVC = 11
    Kafka = 12
    Zookeeper = 13
    ElasticSearch = 14
    Mysql = 15
    SQL = 16
    Tomcat = 17
    SSH = 18

    @staticmethod
    def get_names_by_values(values):
        if values is None:
            return []
        _result = []
        for val in list(ARTICLE_TAGS):
            if val.value in values:
                _result.append(val.name)
        # return [val.name  if val.value in values]
        return _result


class CHROME_PLUGIN_CATEGORY:
    生产工具 = 0
    开发者工具 = 1


class BUSINESS_STATUS:
    成功 = 1000
    失败 = 1001


if __name__ == '__main__':
    print(ARTICLE_TAGS.get_names_by_values([1]))
