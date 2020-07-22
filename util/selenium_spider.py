#!usr/bin/env python
# -*- coding: utf-8 -*-
# fileName: selenium_spider.py
# time: 2020/07/07 23:20

__author__ = '33504'

# browser = webdriver.Chrome()  # 声明浏览器
# url = 'https:www.baidu.com'
# browser.get(url)  # 打开浏览器预设网址
# print(browser.page_source)  # 打印网页源代码
# browser.close()  # 关闭浏览器
#
import json
import logging
import time

from selenium import webdriver  # 导入库

from util.chrome_plugin_spider import ChromePluginSpider

options = webdriver.ChromeOptions();
print(options.arguments)

LOGGER = logging.getLogger(__name__)

PLUGIN_CATEGORY = {
    '开发者工具': {
        'url': 'https://chrome.google.com/webstore/category/ext/11-web-development?utm_source=chrome-ntp-icon',
        'id': '1'
    },
    '生产工具': {
        'url': 'https://chrome.google.com/webstore/category/ext/7-productivity?utm_source=chrome-ntp-icon',
        'id': '0'
    }
}


class SeleniumChromeSpider:

    def __init__(self):
        options = webdriver.ChromeOptions();
        options.add_argument("--auto-open-devtools-for-tabs")
        options.add_argument("--no-sandbox")
        options.add_argument('--proxy-server=socks5://localhost:1080')
        options.add_argument('--headless')
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

        caps = DesiredCapabilities.CHROME
        # as per latest docs
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        self._browser = webdriver.Chrome(options=options, desired_capabilities=caps)
        self._spider = ChromePluginSpider()

    def crawl(self):
        category_ = PLUGIN_CATEGORY["开发者工具"]
        url = category_['url']
        self._browser.get(url)
        for i in range(1000):
            LOGGER.info("selenium {0}".format(i))
            time.sleep(2)
            self._browser.execute_script("window.scrollBy(0, 5000);", {})
            time.sleep(3)
            for entry in self._browser.get_log('performance'):

                try:
                    data = json.loads(entry['message'])
                    method_ = data['message']['method']
                    if 'params' not in data['message']:
                        continue
                    params_ = data['message']['params']
                    if 'type' in params_ and params_['type'] == 'XHR':
                        if 'request' in params_:
                            request_ = params_['request']
                            url_ = request_['url']
                            if url_.find("item") > 0:
                                if 'requestId' in params_:
                                    request_id_ = params_['requestId']
                                    cdp_cmd = self._browser.execute_cdp_cmd("Network.getResponseBody", {'requestId': request_id_})
                                    body_str = cdp_cmd['body'].replace('\n', '')[4:].replace("null", '"null"')
                                    body = json.loads(body_str)
                                    self._spider.handle_item_list_response(body, category_['id'])
                except Exception as e:
                    LOGGER.error(e)
                    time.sleep(300)
                    continue

        self._browser.close()


if __name__ == '__main__':
    spider = SeleniumChromeSpider()
    spider.crawl()
