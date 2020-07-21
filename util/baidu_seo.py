# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/20 18:04
# file_name : baidu_seo.py

import requests

included = ["'http://www.genup.top/article/list-view'"]

to_included = ["http://www.genup.top/article/detail-view/789"]


class CommonInclude:
    def __init__(self, site='www.genup.top', token=None):
        self._url = "http://data.zz.baidu.com/urls?site=www.genup.top&token={token}".format_map({"token": token})

    def include(self, url_arr=[]):
        res = requests.post(self._url, data="\n".join(url_arr))
        print(res.json())


# http://www.genup.top/article/list-view
if __name__ == '__main__':
    include = CommonInclude(token='swafqFNPbTjekabY')
    include.include(to_included)
