# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/06/30 19:20
# file_name : __init__.py.py
from enum import Enum


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


if __name__ == '__main__':
    print(ARTICLE_TYPE.get_name_by_val(1))
