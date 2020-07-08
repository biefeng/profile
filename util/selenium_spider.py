#!usr/bin/env python
# -*- coding: utf-8 -*-
# fileName: selenium_spider.py
# time: 2020/07/07 23:20
from selenium.webdriver import DesiredCapabilities

__author__ = '33504'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from selenium import webdriver  # 导入库

# browser = webdriver.Chrome()  # 声明浏览器
# url = 'https:www.baidu.com'
# browser.get(url)  # 打开浏览器预设网址
# print(browser.page_source)  # 打印网页源代码
# browser.close()  # 关闭浏览器
#
import time, json
from util.chrome_plugin_spider import ChromePluginSpider

options = webdriver.ChromeOptions();
print(options.arguments)


class SeleniumChromeSpider:

	def __init__(self):
		options = webdriver.ChromeOptions();
		options.add_argument("--auto-open-devtools-for-tabs");
		from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

		caps = DesiredCapabilities.CHROME
		# as per latest docs
		caps['goog:loggingPrefs'] = {'performance': 'ALL'}
		self._browser = webdriver.Chrome(options=options, desired_capabilities=caps)
		self._spider = ChromePluginSpider()

	def crawl(self):
		self._browser.get("https://chrome.google.com/webstore/category/ext/7-productivity?utm_source=chrome-ntp-icon")
		while True:
			time.sleep(3)
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
									self._spider.handle_item_list_response(body)
				except Exception as e:
					print(e)
			break

		# self._browser.close()


if __name__ == '__main__':
	spider = SeleniumChromeSpider()
	spider.crawl()
