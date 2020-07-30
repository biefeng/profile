# -*- coding:utf-8 -*-
# author : BieFeNg
# date_time 2020/07/20 18:04
# file_name : baidu_seo.py

import os
from pathlib import Path

import requests

from util.MysqlUtil import Base

included = ["'http://www.genup.top/article/list-view'"]

to_included = ["http://www.genup.top/article/detail-view/789"]


class CommonInclude:
    def __init__(self, site='www.genup.top', token=None):
        self._url = "http://data.zz.baidu.com/urls?site=www.genup.top&token={token}".format_map({"token": token})
        self._mysql = Base("baiduyun", "blog_mini", "root", "Biefeng123!")

    def include(self):
        url_arr = self.find_url()
        interval = 2000
        times = (len(url_arr) + interval - 1) // interval
        for t in range(times):
            start_index = t * interval
            end_index = (t + 1) * interval
            end_index = len(url_arr) if end_index > len(url_arr) else end_index
            tmp_arr = url_arr[start_index:end_index]
            res = requests.post(self._url, data="\n".join(tmp_arr))
            print(res.json())

    def find_url(self):
        urls = []
        mysql = self._mysql
        chrome_plugin_ids = mysql.select("select id from chrome_plugin")
        chrome_plugin_detail_base_url = 'http://www.genup.top//chrome-plugin/detail/{0}'
        for chrome_plugin_id in chrome_plugin_ids.fetchall():
            chrome_plugin_detail_url = chrome_plugin_detail_base_url.format(chrome_plugin_id['id'])
            urls.append(chrome_plugin_detail_url)

        article_ids = mysql.select("select id from articles")
        article_detail_base_url = "http://www.genup.top//article/detail-view/{0}"
        for article_id in article_ids:
            article_detail_url = article_detail_base_url.format(article_id['id'])
            urls.append(article_detail_url)
        print(urls)
        return urls

    def export_to_sitemap_txt(self):
        urls = self.find_url()
        join = "\n".join(urls)
        path = Path(os.getcwd())
        print(path.parent)
        static_dir = os.path.join(str(path.parent), "app\\static")
        with open(static_dir + "\\site.txt", mode="w", encoding="UTF-8") as site_txt:
            site_txt.write(join)
            site_txt.flush()


# http://www.genup.top/article/list-view
if __name__ == '__main__':
    include = CommonInclude(token='swafqFNPbTjekabY')
    # include.include()
    include.export_to_sitemap_txt()

